import hashlib
import os

import psycopg
from dotenv import load_dotenv


load_dotenv(override=True)


def create_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Add it to your .env file."
        )

    return psycopg.connect(
        database_url,
        prepare_threshold=None
    )

def create_tables():
    """Supabase tables are managed in the Supabase SQL Editor."""
    print(
        "Supabase schema is managed remotely; "
        "create_tables() made no changes."
    )


def insert_customer(customer):
    connection = create_connection()
    cursor = connection.cursor()
    
    if customer_exists(customer.customer_id):
        print("Customer already exists.")
        connection.close()
        return
    
    try:
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
            customer.customer_id, 
            customer.full_name, 
            customer.phone, 
            customer.email, 
            customer.address,
            bool(customer.is_active) 
        ))

        connection.commit()
        print("Customer saved to database successfully.")
    except psycopg.IntegrityError:
            print("Error: A customer with this ID already exists.")
    finally :
        connection.close()
    

def view_customers():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    print("\n========== CUSTOMERS IN DATABASE ==========\n")

    for customer in customers:
        print(customer)

    connection.close()
    
def insert_account(account):
    connection = create_connection()
    cursor = connection.cursor()
    
    if account_exists(account.account_number):
        print("Account already exists.")
        connection.close()
        return
    
    try:
         
        cursor.execute("""
            INSERT INTO accounts (
                account_number, 
                customer_id,
                account_type,
                balance,
                is_active
            )
            VALUES (%s, %s, %s, %s, %s)
        """,(
                account.account_number,
                account.customer_id,
                account.account_type,
                account.balance,
                bool(account.is_active) 
             
        ))
        
        connection.commit()
        print("Account saved to database successfully.")
        
    except psycopg.IntegrityError as error:
        print(f"Error saving account: {error}")
        
    finally:
        connection.close()
        
        
def view_accounts():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM accounts")
    
    accounts = cursor.fetchall()
    
    print("\n======= ACCOUNTS IN DATABASE========\n")
    
    for account in accounts: 
        print(account)
    connection.close()
    

def insert_transaction(transaction):
    connection = create_connection()
    cursor = connection.cursor()
    
    try: 
        cursor.execute("""
            INSERT INTO transactions (
                account_number,
                transaction_type,
                amount, 
                status,
                date_created 
            )
            VALUES (%s, %s, %s, %s, %s)
        """,(
            transaction.account_number,
            transaction.transaction_type,
            transaction.amount,
            transaction.status, 
            transaction.date_created
            
        ))
        connection.commit()
        print("Transaction saved to database successfully")
    
    except psycopg.IntegrityError as error:
        print(f"Error saving transaction: {error}")

    finally:
        connection.close()
                      
def view_transaction():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    
    print("\n========== TRANSACTIONS IN DATABASE ===========\n")
    
    if len(transactions) == 0:
        print("No transactions found")
    else: 
        for transaction in transactions:
            print(transaction)
    
    connection.close()
    
    
def update_account_balance(account):
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            UPDATE accounts 
            SET balance = %s 
            WHERE account_number = %s 
        """, (
            account.balance, 
            account.account_number 
            
        ))
        
        connection.commit()
        print("Account balance updated in database.")
    
    finally:
        connection.close()
        
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_login_account(username, password, role, customer_id=None):
    connection = create_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            "SELECT COALESCE(MAX(user_id), 0) + 1 FROM users"
        )
        user_id = cursor.fetchone()[0]

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
            password_hash,
            role,
            True,
            customer_id
        ))

        connection.commit()
        print("Login account created successfully.")
        return True

    except psycopg.IntegrityError as error:
        connection.rollback()
        print(f"Error creating login account: {error}")
        return False

    finally:
        cursor.close()
        connection.close()


def insert_loan(loan):
    connection = create_connection()
    cursor = connection.cursor()

    try:
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
            loan.loan_id,
            loan.customer_id,
            loan.principal,
            loan.annual_interest_rate,
            loan.loan_term_months,
            loan.monthly_installment,
            loan.remaining_balance,
            bool(loan.is_active)
        ))

        connection.commit()
        print("Loan saved to database successfully.")

    except psycopg.IntegrityError as error:
        print(f"Error saving loan: {error}")

    finally:
        connection.close()

def update_loan_balance(loan):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE loans
            SET remaining_balance = %s,
                is_active = %s
            WHERE loan_id = %s
        """, (
            loan.remaining_balance,
            bool(loan.is_active),
            loan.loan_id
        ))

        connection.commit()
        print("Loan balance updated in database.")

    except psycopg.Error as error:
        print(f"Error updating loan: {error}")

    finally:
        connection.close()

def view_loans():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM loans")
    loans = cursor.fetchall()

    print("\n========== LOANS IN DATABASE ==========\n")

    for loan in loans:
        print(loan)

    connection.close()
    
def account_exists(account_number):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM accounts
        WHERE account_number = %s
    """, (account_number,))

    account = cursor.fetchone()

    connection.close()

    return account is not None

def customer_exists(customer_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,))

    customer = cursor.fetchone()

    connection.close()

    return customer is not None

def get_account(account_number):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            account_number,
            customer_id,
            account_type,
            balance,
            is_active
        FROM accounts
        WHERE account_number = %s
    """, (account_number,))

    account_data = cursor.fetchone()

    connection.close()

    return account_data     

def get_all_accounts():
    connection = create_connection()
    cursor = connection.cursor() 
    
    cursor.execute(""" SELECT account_number,
                            customer_id,
                            account_type,
                            balance,
                            is_active
                            FROM accounts 
                            """)
    
    accounts = cursor.fetchall()
    
    connection.close()
    
    return accounts 

def get_all_transactions():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transaction_id,
            account_number,
            transaction_type,
            amount,
            status,
            date_created
        FROM transactions
        ORDER BY transaction_id DESC
    """)

    transactions = cursor.fetchall()

    print("Transactions found:", transactions)

    connection.close()
    
    return transactions
    
def user_exists(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE username = %s",
        (username,)
    )

    result = cursor.fetchone()
    connection.close()

    return result is not None

def insert_user(user):
    connection = create_connection()
    cursor = connection.cursor()

    if user_exists(user.username):
        print("User already exists.")
        connection.close()
        return False

    try:
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
            user.user_id,
            user.username,
            user.password,
            user.role,
            bool(user.is_active),
            user.customer_id
        ))

        connection.commit()
        print("User saved successfully.")
        return True

    except psycopg.Error as error:
        print(f"Error saving user: {error}")
        return False

    finally:
        connection.close()
        
def get_user_by_username(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            user_id,
            username,
            password,
            is_active,
            customer_id,
            role,
            failed_login_attempts
        FROM users
        WHERE username = %s
    """, (username,))

    user = cursor.fetchone()

    connection.close()

    return user

    


def add_customer_id_to_users():
    """Deprecated: the Supabase users table already has customer_id."""
    print("customer_id already exists in the Supabase schema.")


def add_role_to_users():
    """Deprecated: the Supabase users table already has role."""
    print("role already exists in the Supabase schema.")


def get_accounts_by_customer(customer_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
            SELECT 
                account_number,
                customer_id,
                account_type,
                balance,
                is_active
            FROM accounts
            WHERE customer_id = %s
    """, (customer_id,))

    accounts = cursor.fetchall()
    connection.close()
    return accounts 

                   
def link_user_to_customer(username, customer_id):
    connection = create_connection()
    cursor= connection.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET customer_id = %s 
        WHERE username = %s 
    """, (
        customer_id,
        username
    ))
    
    connection.commit()
    connection.close()
    
    print("User linked to customer successfully.")
                           
    
def get_transactions_by_customer(customer_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transactions.transaction_id,
            transactions.account_number,
            transactions.transaction_type,
            transactions.amount,
            transactions.status,
            transactions.date_created
        FROM transactions
        INNER JOIN accounts
            ON transactions.account_number = accounts.account_number
        WHERE accounts.customer_id = %s
        ORDER BY transactions.transaction_id DESC
    """, (customer_id,))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def update_user_status(user_id, is_active):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        if is_active:
            cursor.execute("""
                UPDATE users
                SET
                    is_active = TRUE,
                    failed_login_attempts = 0
                WHERE user_id = %s
            """, (user_id,))
        else:
            cursor.execute("""
                UPDATE users
                SET is_active = FALSE
                WHERE user_id = %s
            """, (user_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()



def increment_failed_login_attempts(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET failed_login_attempts = failed_login_attempts + 1
            WHERE user_id = %s
            RETURNING failed_login_attempts
        """, (user_id,))

        result = cursor.fetchone()
        connection.commit()

        if result is None:
            return None

        return result[0]

    finally:
        cursor.close()
        connection.close()


def reset_failed_login_attempts(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET failed_login_attempts = 0
            WHERE user_id = %s
        """, (user_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def deactivate_user_after_failed_logins(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE users
            SET is_active = FALSE
            WHERE user_id = %s
        """, (user_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def delete_user(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE user_id = %s
    """, (user_id,))

    connection.commit()
    connection.close()

def get_all_users():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            user_id,
            username,
            role,
            is_active,
            customer_id
        FROM users
        ORDER BY user_id
    """)

    users = cursor.fetchall()

    connection.close()

    return users

def get_analytics_summary():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(balance), 0)
        FROM accounts
    """)
    total_balance = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM loans")
    total_loans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE is_active = TRUE
    """)
    active_users = cursor.fetchone()[0]

    connection.close()

    return {
        "total_customers": total_customers,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "total_transactions": total_transactions,
        "total_loans": total_loans,
        "active_users": active_users
    }
    
def get_transactions_by_type():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT
            transaction_type,
            COUNT(*)
        FROM transactions
        GROUP BY transaction_type
        ORDER BY transaction_type
    """)
    
    results = cursor.fetchall()
    connection.close()
    
    return results 


def get_accounts_by_type():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT
            account_type,
            COUNT(*)
        FROM accounts
        GROUP BY account_type
        ORDER BY account_type
    """)
    
    results = cursor.fetchall()
    connection.close()
    
    return results 

def get_recent_transactions(limit=5):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT 
            transaction_id,
            account_number,
            transaction_type,
            amount,
            status,
            date_created
        FROM transactions
        ORDER BY transaction_id DESC
        LIMIT %s
    """, (limit,))
    
    transactions = cursor.fetchall()
    connection.close()
    
    return transactions 


def get_top_account_balances(limit=5):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT
            accounts.account_number,
            customers.full_name,
            accounts.account_type,
            accounts.balance
        FROM accounts
        INNER JOIN customers
            ON accounts.customer_id = customers.customer_id
        ORDER BY accounts.balance DESC
        LIMIT %s
    """, (limit,)) 
    
    accounts = cursor.fetchall()
    connection.close()
    return accounts 

def get_customer_financial_details(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT 
            users.user_id,
            users.username,
            users.customer_id,
            customers.full_name,
            accounts.account_number,
            accounts.account_type,
            accounts.balance,
            accounts.is_active
        FROM users
        INNER JOIN customers
            ON users.customer_id = customers.customer_id
        INNER JOIN accounts 
            ON customers.customer_id = accounts.customer_id
        WHERE users.user_id = %s
    """,(user_id,))
    
    customer_details = cursor.fetchone()
    
    if customer_details is None:
        connection.close()
        return None, []
    
    account_number = customer_details[4]
    
    cursor.execute("""
        SELECT
            transaction_id,
            transaction_type,
            amount,
            status,
            date_created
        FROM transactions
        WHERE account_number = %s
        ORDER BY transaction_id DESC
    """, (account_number,))
    
    transactions = cursor.fetchall()
    connection.close()
    return customer_details, transactions