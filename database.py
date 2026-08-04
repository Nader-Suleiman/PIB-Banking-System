import sqlite3
import hashlib 

def create_connection():
    connection = sqlite3.connect("banking_system.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection 

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Customer',
    is_active INTEGER NOT NULL,
    customer_id INTEGER
)
""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            is_active INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            date_created TEXT NOT NULL,

            FOREIGN KEY (account_number)
            REFERENCES accounts(account_number)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id TEXT PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            principal REAL NOT NULL,
            annual_interest_rate REAL NOT NULL,
            loan_term_months INTEGER NOT NULL,
            monthly_installment REAL NOT NULL,
            remaining_balance REAL NOT NULL,
            is_active INTEGER NOT NULL,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully.")
    
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
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer.customer_id, 
            customer.full_name, 
            customer.phone, 
            customer.email, 
            customer.address,
            1 if customer.is_active else 0 
        ))

        connection.commit()
        print("Customer saved to database successfully.")
    except sqlite3.IntegrityError:
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
            VALUES (?, ?, ?, ?, ?)
        """,(
                account.account_number,
                account.customer_id,
                account.account_type,
                account.balance,
                1 if account.is_active else 0 
             
        ))
        
        connection.commit()
        print("Account saved to database successfully.")
        
    except sqlite3.IntegrityError as error:
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
            VALUES (?, ?, ?, ?, ?)
        """,(
            transaction.account_number,
            transaction.transaction_type,
            transaction.amount,
            transaction.status, 
            transaction.date_created
            
        ))
        connection.commit()
        print("Transaction saved to database successfully")
    
    except sqlite3.IntegrityError as error:
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
            SET balance = ? 
            WHERE account_number = ? 
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
        cursor.execute("""
            INSERT INTO login_users (
                username,
                password_hash,
                role,
                customer_id
            )
            VALUES (?, ?, ?, ?)
        """, (
            username,
            password_hash,
            role,
            customer_id
        ))

        connection.commit()
        print("Login account created successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Error creating login account: {error}")

    finally:
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
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            loan.loan_id,
            loan.customer_id,
            loan.principal,
            loan.annual_interest_rate,
            loan.loan_term_months,
            loan.monthly_installment,
            loan.remaining_balance,
            1 if loan.is_active else 0
        ))

        connection.commit()
        print("Loan saved to database successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Error saving loan: {error}")

    finally:
        connection.close()

def update_loan_balance(loan):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE loans
            SET remaining_balance = ?,
                is_active = ?
            WHERE loan_id = ?
        """, (
            loan.remaining_balance,
            1 if loan.is_active else 0,
            loan.loan_id
        ))

        connection.commit()
        print("Loan balance updated in database.")

    except sqlite3.Error as error:
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
        WHERE account_number = ?
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
        WHERE customer_id = ?
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
        WHERE account_number = ?
    """, (account_number,))

    account_data = cursor.fetchone()

    connection.close()

    return account_data     

def get_all_accounts():
    connection = sqlite3.connect("banking_system.db")
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
        "SELECT 1 FROM users WHERE username = ?",
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
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user.user_id,
            user.username,
            user.password,
            user.role,
            1 if user.is_active else 0,
            user.customer_id
        ))

        connection.commit()
        print("User saved successfully.")
        return True

    except sqlite3.Error as error:
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
            role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    connection.close()

    return user

    


def add_customer_id_to_users():
    connection = create_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN customer_id INTEGER
        """)
        
        connection.commit()
        print("customer_id added to users table.")
        
    except sqlite3.OperationalError as error:
        if "duplicate column name" in str(error):
            print("customer_id already exists in users table.")
        else:
            print(f"Error updating users table: {error}")
            
    finally:
        connection.close()
        
def add_role_to_users():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN role TEXT NOT NULL DEFAULT 'Customer'
        """)

        connection.commit()
        print("Role column added successfully.")

    except sqlite3.OperationalError as error:
        if "duplicate column name" in str(error):
            print("Role column already exists.")
        else:
            print(error)

    finally:
        connection.close()
        
                       
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
            WHERE customer_id = ?
    """, (customer_id,))

    accounts = cursor.fetchall()
    connection.close()
    return accounts 

                   
def link_user_to_customer(username, customer_id):
    connection = create_connection()
    cursor= connection.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET customer_id = ? 
        WHERE username = ? 
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
        WHERE accounts.customer_id = ?
        ORDER BY transactions.transaction_id DESC
    """, (customer_id,))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def update_user_status(user_id, is_active):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET is_active = ?
        WHERE user_id = ?
    """, (
        1 if is_active else 0,
        user_id
    ))

    connection.commit()
    connection.close()


def delete_user(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE user_id = ?
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
        WHERE is_active = 1
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
        LIMIT ?
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
        LIMIT ?
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
        WHERE users.user_id = ?
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
        WHERE account_number = ?
        ORDER BY transaction_id DESC
    """, (account_number,))
    
    transactions = cursor.fetchall()
    connection.close()
    return customer_details, transactions

    
    