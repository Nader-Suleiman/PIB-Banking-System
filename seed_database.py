import os
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

import psycopg
from dotenv import load_dotenv


load_dotenv(override=True)

CUSTOMER_COUNT = 50
TRANSACTION_COUNT = 500
LOAN_COUNT = 18

random.seed(42)


FIRST_NAMES = [
    "Omar", "Ahmad", "Mohammad", "Yousef", "Khaled",
    "Ali", "Mahmoud", "Tareq", "Samer", "Laith",
    "Lina", "Mariam", "Sara", "Noor", "Rana",
    "Hala", "Dalia", "Ruba", "Aya", "Reem"
]

LAST_NAMES = [
    "Nader", "Khalil", "Hamdan", "Ibrahim", "Saleh",
    "Suleiman", "Hassan", "Qasem", "Darwish", "Mansour",
    "Barakat", "Awad", "Shalabi", "Tamimi", "Masri"
]

CITIES = [
    "Ramallah",
    "Nablus",
    "Hebron",
    "Bethlehem",
    "Jenin",
    "Jericho",
    "Tulkarm",
    "Qalqilya"
]

ACCOUNT_TYPES = [
    "Savings",
    "Checking"
]


def create_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing from the .env file."
        )

    return psycopg.connect(
        database_url,
        prepare_threshold=None
    )


def random_date_within_last_six_months():
    days_ago = random.randint(0, 180)

    random_date = (
        datetime.now()
        - timedelta(days=days_ago)
    )

    return random_date.replace(
        hour=random.randint(8, 18),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=0
    )


def generate_unique_name(existing_names):
    while True:
        full_name = (
            f"{random.choice(FIRST_NAMES)} "
            f"{random.choice(LAST_NAMES)}"
        )

        if full_name not in existing_names:
            existing_names.add(full_name)
            return full_name


def calculate_monthly_installment(
    principal,
    annual_interest_rate,
    loan_term_months
):
    monthly_rate = annual_interest_rate / 100 / 12

    if monthly_rate == 0:
        return principal / loan_term_months

    return (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** loan_term_months
    ) / (
        (1 + monthly_rate) ** loan_term_months - 1
    )


def clear_old_demo_data(cursor):
    print("Removing old demo data...")

    cursor.execute("""
        TRUNCATE TABLE
            audit_logs,
            transactions,
            loans,
            accounts,
            users,
            customers
        RESTART IDENTITY CASCADE
    """)


def create_staff_users(cursor):
    print("Creating Admin and Teller users...")

    staff_users = [
        (
            9001,
            "admin",
            generate_password_hash("admin123"),
            "Admin",
            True,
            None
        ),
        (
            123,
            "teller",
            generate_password_hash("teller123"),
            "Teller",
            True,
            None
        )
    ]

    cursor.executemany("""
        INSERT INTO users (
            user_id,
            username,
            password,
            role,
            is_active,
            customer_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, staff_users)


def create_customers_accounts_and_users(cursor):
    print("Creating customers, accounts, and users...")

    account_balances = {}
    customer_ids = []
    account_numbers = []
    existing_names = set()

    for index in range(1, CUSTOMER_COUNT + 1):
        customer_id = 10000 + index
        user_id = 20000 + index
        account_number = f"ACC{30000 + index}"

        full_name = generate_unique_name(existing_names)

        username = (
            full_name
            .lower()
            .replace(" ", ".")
            + str(index)
        )

        password = generate_password_hash("demo123")

        phone_prefix = random.choice(["056", "059"])
        phone = (
            phone_prefix
            + str(random.randint(1000000, 9999999))
        )

        email_name = (
            full_name
            .lower()
            .replace(" ", ".")
        )

        email = f"{email_name}{index}@example.com"
        address = f"{random.choice(CITIES)}, Palestine"
        account_type = random.choice(ACCOUNT_TYPES)

        initial_balance = round(
            random.uniform(1000, 45000),
            2
        )

        cursor.execute("""
            INSERT INTO customers (
                customer_id,
                full_name,
                phone,
                email,
                address,
                is_active
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            customer_id,
            full_name,
            phone,
            email,
            address,
            True
        ))

        cursor.execute("""
            INSERT INTO users (
                user_id,
                username,
                password,
                role,
                is_active,
                customer_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            username,
            password,
            "Customer",
            True,
            customer_id
        ))

        cursor.execute("""
            INSERT INTO accounts (
                account_number,
                customer_id,
                account_type,
                balance,
                is_active
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            account_number,
            customer_id,
            account_type,
            initial_balance,
            True
        ))

        customer_ids.append(customer_id)
        account_numbers.append(account_number)
        account_balances[account_number] = initial_balance

    return customer_ids, account_numbers, account_balances


def add_transaction(
    cursor,
    account_number,
    transaction_type,
    amount,
    date_created
):
    cursor.execute("""
        INSERT INTO transactions (
            account_number,
            transaction_type,
            amount,
            status,
            date_created
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        account_number,
        transaction_type,
        round(amount, 2),
        "Completed",
        date_created
    ))


def create_transactions(
    cursor,
    account_numbers,
    account_balances
):
    print("Creating transactions...")

    for _ in range(TRANSACTION_COUNT):
        transaction_choice = random.choices(
            ["Deposit", "Withdrawal", "Transfer"],
            weights=[45, 30, 25],
            k=1
        )[0]

        date_created = random_date_within_last_six_months()

        if transaction_choice == "Deposit":
            account_number = random.choice(account_numbers)

            amount = round(
                random.uniform(50, 5000),
                2
            )

            account_balances[account_number] += amount

            add_transaction(
                cursor,
                account_number,
                "Deposit",
                amount,
                date_created
            )

        elif transaction_choice == "Withdrawal":
            account_number = random.choice(account_numbers)
            current_balance = account_balances[account_number]

            maximum_withdrawal = min(
                3000,
                current_balance * 0.35
            )

            if maximum_withdrawal < 20:
                continue

            amount = round(
                random.uniform(20, maximum_withdrawal),
                2
            )

            account_balances[account_number] -= amount

            add_transaction(
                cursor,
                account_number,
                "Withdrawal",
                amount,
                date_created
            )

        else:
            sender_account = random.choice(account_numbers)

            receiver_account = random.choice([
                account
                for account in account_numbers
                if account != sender_account
            ])

            sender_balance = account_balances[sender_account]

            maximum_transfer = min(
                4000,
                sender_balance * 0.25
            )

            if maximum_transfer < 25:
                continue

            amount = round(
                random.uniform(25, maximum_transfer),
                2
            )

            account_balances[sender_account] -= amount
            account_balances[receiver_account] += amount

            add_transaction(
                cursor,
                sender_account,
                "Transfer Out",
                amount,
                date_created
            )

            add_transaction(
                cursor,
                receiver_account,
                "Transfer In",
                amount,
                date_created
            )

    for account_number, balance in account_balances.items():
        cursor.execute("""
            UPDATE accounts
            SET balance = %s
            WHERE account_number = %s
        """, (
            round(balance, 2),
            account_number
        ))


def create_loans(cursor, customer_ids):
    print("Creating loans...")

    selected_customers = random.sample(
        customer_ids,
        LOAN_COUNT
    )

    for index, customer_id in enumerate(
        selected_customers,
        start=1
    ):
        loan_id = f"LN{40000 + index}"

        principal = round(
            random.uniform(3000, 50000),
            2
        )

        annual_interest_rate = random.choice([
            3.5,
            4.0,
            4.5,
            5.0,
            5.5,
            6.0,
            6.5
        ])

        loan_term_months = random.choice([
            12,
            24,
            36,
            48,
            60
        ])

        monthly_installment = calculate_monthly_installment(
            principal,
            annual_interest_rate,
            loan_term_months
        )

        amount_repaid = random.uniform(
            0,
            principal * 0.45
        )

        remaining_balance = max(
            principal - amount_repaid,
            0
        )

        cursor.execute("""
            INSERT INTO loans (
                loan_id,
                customer_id,
                principal,
                annual_interest_rate,
                loan_term_months,
                monthly_installment,
                remaining_balance,
                is_active
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            loan_id,
            customer_id,
            principal,
            annual_interest_rate,
            loan_term_months,
            round(monthly_installment, 2),
            round(remaining_balance, 2),
            True
        ))


def print_summary(cursor):
    print("\n========== SUPABASE DEMO SUMMARY ==========")

    for label, table_name in [
        ("Users", "users"),
        ("Customers", "customers"),
        ("Accounts", "accounts"),
        ("Transactions", "transactions"),
        ("Loans", "loans")
    ]:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )
        print(f"{label}: {cursor.fetchone()[0]}")

    cursor.execute("""
        SELECT COALESCE(SUM(balance), 0)
        FROM accounts
    """)

    total_balance = cursor.fetchone()[0]

    print(f"Total balance: ${total_balance:,.2f}")

    print("\nDemo logins:")
    print("Admin: admin / admin123")
    print("Teller: teller / teller123")
    print("Customers: generated username / demo123")


def seed_database():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        clear_old_demo_data(cursor)
        create_staff_users(cursor)

        (
            customer_ids,
            account_numbers,
            account_balances
        ) = create_customers_accounts_and_users(cursor)

        create_transactions(
            cursor,
            account_numbers,
            account_balances
        )

        create_loans(
            cursor,
            customer_ids
        )

        connection.commit()
        print_summary(cursor)

        print("\nSupabase database seeded successfully.")

    except psycopg.Error as error:
        connection.rollback()
        print(f"\nDatabase seeding failed: {error}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    seed_database()