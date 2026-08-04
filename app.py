from flask import Flask, render_template, request, flash, redirect, url_for, session

from account import Account
from customer import Customer
from loan import Loan
from user import User
from database import (create_tables,get_account,get_all_accounts,get_all_transactions,insert_transaction,update_account_balance, insert_loan, customer_exists,insert_customer, insert_account, account_exists, insert_user, user_exists, get_user_by_username,add_customer_id_to_users,get_accounts_by_customer,
link_user_to_customer,get_transactions_by_customer,add_role_to_users,get_all_users,update_user_status,delete_user,get_analytics_summary,get_transactions_by_type,get_accounts_by_type, get_recent_transactions,get_top_account_balances,get_customer_financial_details)

from helpers import(login_required,is_customer,is_teller,is_admin,is_staff)

app = Flask(__name__)

app.secret_key = "banking_secret_key"


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    role = session.get("role")

    if role == "Admin":
        return redirect(url_for("admin_dashboard"))

    if role == "Teller":
        return redirect(url_for("teller_dashboard"))

    return render_template("index.html")

@app.route("/deposit", methods=["GET", "POST"])
def deposit_page():

    if request.method == "POST":

        account_number = request.form.get(
            "account_number",
            ""
        ).strip()

        amount_text = request.form.get(
            "amount",
            ""
        ).strip()

        if not account_number:
            flash(
                "Please enter an account number.",
                "error"
            )
            return redirect(url_for("deposit_page"))

        try:
            amount = float(amount_text)

        except ValueError:
            flash(
                "Please enter a valid deposit amount.",
                "error"
            )
            return redirect(url_for("deposit_page"))

        if amount <= 0:
            flash(
                "Deposit amount must be greater than zero.",
                "error"
            )
            return redirect(url_for("deposit_page"))

        account_data = get_account(account_number)

        if account_data is None:
            flash(
                "Account was not found.",
                "error"
            )
            return redirect(url_for("deposit_page"))

        account_record = Account(
            account_number=account_data[0],
            customer_id=account_data[1],
            account_type=account_data[2],
            balance=account_data[3]
        )

        account_record.is_active = bool(account_data[4])

        if not account_record.is_active:
            flash(
                "This account is inactive.",
                "error"
            )
            return redirect(url_for("deposit_page"))

        previous_transaction_count = len(
            account_record.transactions
        )

        account_record.deposit(amount)

        if (
            len(account_record.transactions)
            > previous_transaction_count
        ):

            insert_transaction(
                account_record.transactions[-1]
            )

            update_account_balance(account_record)

            flash(
                f"Deposit successful. New balance: "
                f"${account_record.balance:.2f}",
                "success"
            )

        else:
            flash(
                "The deposit could not be completed.",
                "error"
            )

        return redirect(url_for("deposit_page"))

    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET" , "POST"])
def withdraw_page():
    
    if request.method == "POST":
        account_number = request.form.get("account_number", "").strip()
        amount_text = request.form.get("amount", "").strip()
        
        if not account_number:
            flash("Please enter an account number.", "error")
            return redirect(url_for("withdraw_page"))
        
        try:
            amount = float(amount_text)
        
        except ValueError:
            flash("Please Enter a valid withdrawal amount." , "error")
            return redirect(url_for("withdraw_page"))
        
        if amount <= 0: 
            flash("Withdrawal amount must be greater than 0" , "error")
            return redirect(url_for("withdraw_page"))
        account_data = get_account(account_number)
        
        if account_data is None:
            flash("Account was not found." , "error")
            return redirect(url_for("withdraw_page"))
        
        account_record = Account(account_number = account_data[0], customer_id = account_data[1], account_type = account_data[2], balance=account_data[3])
        
        account_record.is_active = bool(account_data[4])
        
        if not account_record.is_active:
            flash("This account is inactive." , "error")
            return redirect(url_for("withdraw_page"))
        
        if amount > account_record.balance:
            flash("Insufficient funds." , "error")
            return redirect(url_for("withdraw_page"))
        
        previous_transaction_count = len(account_record.transactions)
        account_record.withdraw(amount)
        
        if len(account_record.transactions) > previous_transaction_count:
            
            insert_transaction(account_record.transactions[-1])
            update_account_balance(account_record)
            
            flash(f"Withdrawal successful. Remaining balance: "
                  f"${account_record.balance:.2f}",
                  "success")
        else:
            flash("The withdrawal could not be completed." , "error")
            
        return redirect(url_for("withdraw_page"))
      
    return render_template("withdraw.html")


@app.route("/transfer", methods=["GET", "POST"])
def transfer_page():
    
    if request.method == "POST":
        
        sender_account_number = request.form.get("sender_account_number", "").strip()
        
        receiver_account_number = request.form.get("receiver_account_number", "").strip()
        
        amount_text = request.form.get("amount", "").strip()
        
        if not sender_account_number:
            flash("Please enter the sender account number.", "error")
            return redirect(url_for("transfer_page"))
        
        if not receiver_account_number:
            flash("Please enter the receiver account number." , "error")
            return redirect(url_for("transfer_page"))
        
        if sender_account_number == receiver_account_number:
            flash("sender and receiver account cannot be the same" , "error")
            return redirect(url_for("transfer_page"))
        
        try:
            amount = float(amount_text)
            
        except ValueError:
            flash("Please enter a valid transfer account." , "error")
            return redirect(url_for("transfer_page"))
        
        if amount <= 0:
            flash("Transfer amount must be greater than 0." , "error")
            return redirect(url_for("transfer_page"))
        
        sender_data = get_account(sender_account_number)
        receiver_data = get_account(receiver_account_number)
        
        if sender_data is None:
            flash("Sender account was not found.", "error")
            return redirect(url_for("transfer_page"))
        
        if receiver_data is None:
            flash("receiver account was not found." , "error")
            return redirect(url_for("transfer_page"))
        
        sender_account = Account(account_number=sender_data[0],customer_id=sender_data[1], account_type=sender_data[2],balance=sender_data[3])
        
        sender_account.is_active = bool(sender_data[4])
        
        receiver_account = Account(account_number=receiver_data[0], customer_id=receiver_data[1], account_type=receiver_data[2],balance=receiver_data[3])
        receiver_account.is_active = bool(receiver_data[4]) 
        
        if not sender_account.is_active:
            flash("Sender account is inactive." , "error")
            return redirect(url_for("transfer_page"))
        
        if not receiver_account.is_active:
            flash("Receiver account is inactive." , "error")
            return redirect(url_for("transfer_page"))
        
        if amount > sender_account.balance:
            flash("Insufficient funds in sender account." , "error")
            return redirect(url_for("transfer_page"))
        
        sender_transaction_count = len(sender_account.transactions)
        recevier_transaction_count = len(receiver_account.transactions)
        
        sender_account.transfer(receiver_account, amount)
        
        if len(sender_account.transactions) > sender_transaction_count and len(receiver_account.transactions) > recevier_transaction_count:
            
            insert_transaction(sender_account.transactions[-1])
            insert_transaction(receiver_account.transactions[-1])
            
            update_account_balance(sender_account)
            update_account_balance(receiver_account)
            
            flash(f"Transfer successful. " 
                  f"Sender Balance: ${sender_account.balance:.2f}",
                  "success")
            
        else:
            flash("The transfer could not be completed." ,"error")
        return redirect(url_for("transfer_page"))
        
    return render_template("transfer.html")

@app.route("/accounts")
def accounts_page():

    if "customer_id" not in session:
        return redirect(url_for("login_page"))

    accounts = get_accounts_by_customer(
        session["customer_id"]
    )

    return render_template(
        "accounts.html",
        accounts=accounts
    )
    
@app.route("/transactions")
def transactions_page():

    if "customer_id" not in session:
        return redirect(url_for("login_page"))

    transactions = get_transactions_by_customer(
        session["customer_id"]
    )

    return render_template(
        "transactions.html",
        transactions=transactions
    )

@app.route("/loans/create", methods=["GET", "POST"])
def create_loan_page():

    if request.method == "POST":

        loan_id = request.form.get("loan_id", "").strip()
        customer_id_text = request.form.get(
            "customer_id", ""
        ).strip()
        principal_text = request.form.get(
            "principal", ""
        ).strip()
        interest_rate_text = request.form.get(
            "annual_interest_rate", ""
        ).strip()
        term_text = request.form.get(
            "loan_term_months", ""
        ).strip()

        if not loan_id:
            flash("Please enter a loan ID.", "error")
            return redirect(url_for("create_loan_page"))

        try:
            customer_id = int(customer_id_text)
            principal = float(principal_text)
            annual_interest_rate = float(
                interest_rate_text
            )
            loan_term_months = int(term_text)

        except ValueError:
            flash(
                "Please enter valid numerical values.",
                "error"
            )
            return redirect(url_for("create_loan_page"))

        if not customer_exists(customer_id):
            flash("Customer was not found.", "error")
            return redirect(url_for("create_loan_page"))

        if principal <= 0:
            flash(
                "Loan amount must be greater than zero.",
                "error"
            )
            return redirect(url_for("create_loan_page"))

        if annual_interest_rate < 0:
            flash(
                "Interest rate cannot be negative.",
                "error"
            )
            return redirect(url_for("create_loan_page"))

        if loan_term_months <= 0:
            flash(
                "Loan term must be greater than zero.",
                "error"
            )
            return redirect(url_for("create_loan_page"))

        loan = Loan(
            loan_id=loan_id,
            customer_id=customer_id,
            principal=principal,
            annual_interest_rate=annual_interest_rate,
            loan_term_months=loan_term_months
        )

        payment_schedule = loan.get_payment_schedule()

        total_repayment = sum(
            payment["payment_amount"]
            for payment in payment_schedule
        )

        total_interest = (
            total_repayment - loan.principal
        )

        insert_loan(loan)

        flash(
            "Loan calculated and created successfully.",
            "success"
        )

        return render_template(
            "create_loan.html",
            loan=loan,
            payment_schedule=payment_schedule,
            total_repayment=total_repayment,
            total_interest=total_interest
        )

    return render_template(
        "create_loan.html",
        loan=None,
        payment_schedule=None
    )

@app.route("/create-account" , methods=["GET","POST"])
def create_account_page():
    if request.method == "POST":
        user_id_text = request.form.get("user_id" , "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password" , "").strip()
        
        customer_id_text = request.form.get("customer_id", "").strip()
        
        full_name = request.form.get("full_name", "").strip()
        
        phone = request.form.get("phone", "").strip()
        
        email = request.form.get("email", "").strip()
        
        address = request.form.get("address", "").strip()
        
        account_number = request.form.get("account_number", "").strip()
        
        account_type = request.form.get("account_type", "").strip()
        
        initial_deposit_text = request.form.get("initial_deposit", "").strip()
        
        if not username:
            flash("Please enter a username." ,"error")
            return redirect( url_for("create_account_page"))
        
        if not password:
            flash("Please enter a password." , "error")
            return redirect ( url_for("create_account_page"))
        
        if not full_name:
            flash("Please enter the customers full name." , "error")
            return redirect ( url_for("create_account_page "))
        
        if not account_number:
            flash("Please enter an account number." , "error")
            return redirect ( url_for("create_account_page"))
        
        if not account_type:
            flash("Please enter account type." , "error")
            return redirect (url_for("create_account_page"))
        
        try:
            user_id = int(user_id_text)
            customer_id = int(customer_id_text)
            initial_deposit = float(initial_deposit_text)
            
        except ValueError:
            flash("Please enter valid numerical values.", "error")
            return redirect( url_for("create_account_page"))
        
        if initial_deposit < 0:
            flash("Initial deposit cannot be negative.", "error")
            return redirect( url_for("create_account_page"))
        
        if customer_exists(customer_id):
            flash("A customer with this ID already exists.","error")
            return redirect(url_for("create_account_page"))

        if account_exists(account_number):
            flash("An account with this number already exists.","error")
            return redirect(url_for("create_account_page"))
        
        if user_exists(username):
            flash("This username already exists.", "error")
            return redirect(url_for("create_account_page"))
        
        user = User(user_id=user_id,username=username,password=password,customer_id=customer_id)

        customer = Customer(user_id=user_id,username=username,password=password,customer_id=customer_id,full_name=full_name,phone=phone,email=email,address=address)

        account = Account(account_number=account_number,customer_id=customer_id,account_type=account_type,balance=initial_deposit)

        insert_user(user)
        insert_customer(customer)
        insert_account(account)

        flash("Customer and bank account created successfully.","success")

        return redirect(url_for("create_account_page"))

    return render_template("create_account.html")

@app.route("/")
def root():
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET", "POST"])
def login_page():

    # Clear old queued flash messages when opening the login page
    if request.method == "GET":
        session.pop("_flashes", None)

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = get_user_by_username(username)

        if user is None:
            flash("Username not found.", "error")
            return redirect(url_for("login_page"))

        saved_password = user[2]
        is_active = user[3]
        customer_id = user[4]
        role = user[5]

        if password != saved_password:
            flash("Incorrect password.", "error")
            return redirect(url_for("login_page"))

        if not is_active:
            flash("This user account is inactive.", "error")
            return redirect(url_for("login_page"))

        session["user_id"] = user[0]
        session["username"] = user[1]
        session["customer_id"] = customer_id
        session["role"] = role

        if role == "Admin":
            return redirect(url_for("admin_dashboard"))

        elif role == "Teller":
            return redirect(url_for("teller_dashboard"))

        else:
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("dashboard"))
    
    summary = get_analytics_summary()
    transaction_data = get_transactions_by_type()
    account_data = get_accounts_by_type()
    recent_transactions = get_recent_transactions()
    
    transaction_labels = [row[0] for row in transaction_data]
    
    transaction_values = [row[1] for row in transaction_data]
    
    account_labels = [row[0] for row in account_data]
    
    account_values = [row[1] for row in account_data]
    
    return render_template("admin_dashboard.html", 
        summary = summary,
        transaction_labels=transaction_labels,
        transaction_values=transaction_values,
        account_labels=account_labels,
        account_values=account_values,
        recent_transactions=recent_transactions)


@app.route("/teller-dashboard")
def teller_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Teller":
        flash("Access denied.", "error")
        return redirect(url_for("dashboard"))

    return render_template("teller_dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login_page"))  


@app.route("/admin/create-teller", methods=["GET", "POST"])
def create_teller_page():
    
    print("CURRENT ROLE:", session.get("role"))

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    if request.method == "POST":

        user_id_text = request.form.get("user_id", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username:
            flash("Please enter a username.", "error")
            return redirect(url_for("create_teller_page"))

        if not password:
            flash("Please enter a password.", "error")
            return redirect(url_for("create_teller_page"))

        try:
            user_id = int(user_id_text)

        except ValueError:
            flash("Please enter a valid user ID.", "error")
            return redirect(url_for("create_teller_page"))

        if user_exists(username):
            flash("This username already exists.", "error")
            return redirect(url_for("create_teller_page"))

        teller = User(
            user_id=user_id,
            username=username,
            password=password,
            customer_id=None,
            role="Teller"
        )

        if insert_user(teller):
            flash("Teller created successfully.", "success")
        else:
            flash("The teller could not be created.", "error")

        return redirect(url_for("create_teller_page"))

    return render_template("create_staff.html", staff_role="Teller")  

@app.route("/admin/create-admin", methods=["GET", "POST"])
def create_admin_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    if request.method == "POST":

        user_id_text = request.form.get("user_id", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username:
            flash("Please enter a username.", "error")
            return redirect(url_for("create_admin_page"))

        if not password:
            flash("Please enter a password.", "error")
            return redirect(url_for("create_admin_page"))

        try:
            user_id = int(user_id_text)

        except ValueError:
            flash("Please enter a valid user ID.", "error")
            return redirect(url_for("create_admin_page"))

        if user_exists(username):
            flash("This username already exists.", "error")
            return redirect(url_for("create_admin_page"))

        admin_user = User(
            user_id=user_id,
            username=username,
            password=password,
            customer_id=None,
            role="Admin"
        )

        if insert_user(admin_user):
            flash("Admin created successfully.", "success")
        else:
            flash("The admin could not be created.", "error")

        return redirect(url_for("create_admin_page"))

    return render_template(
        "create_staff.html",
        staff_role="Admin"
    )      

@app.route("/admin/accounts")
def admin_accounts():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    accounts = get_all_accounts()

    return render_template(
        "accounts.html",
        accounts=accounts
    )
    

@app.route("/admin/transactions")
def admin_transactions():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    transactions = get_all_transactions()

    return render_template(
        "transactions.html",
        transactions=transactions
    )
    
@app.route("/admin/users")
def user_management_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    users = get_all_users()

    return render_template(
        "user_management.html",
        users=users
    )


@app.route("/admin/users/<int:user_id>/activate", methods=["POST"])
def activate_user(user_id):

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    update_user_status(user_id, True)

    flash("User activated successfully.", "success")
    return redirect(url_for("user_management_page"))


@app.route("/admin/users/<int:user_id>/deactivate", methods=["POST"])
def deactivate_user(user_id):

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    if user_id == session.get("user_id"):
        flash("You cannot deactivate your own admin account.", "error")
        return redirect(url_for("user_management_page"))

    update_user_status(user_id, False)

    flash("User deactivated successfully.", "success")
    return redirect(url_for("user_management_page"))


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
def remove_user(user_id):

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    if user_id == session.get("user_id"):
        flash("You cannot delete your own admin account.", "error")
        return redirect(url_for("user_management_page"))

    delete_user(user_id)

    flash("User login account deleted successfully.", "success")
    return redirect(url_for("user_management_page"))

@app.route("/teller/accounts")
def teller_accounts():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") not in ["Teller", "Admin"]:
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    accounts = get_all_accounts()

    return render_template(
        "accounts.html",
        accounts=accounts
    )


@app.route("/teller/transactions")
def teller_transactions():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") not in ["Teller", "Admin"]:
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    transactions = get_all_transactions()

    return render_template(
        "transactions.html",
        transactions=transactions
    )
    
@app.route("/admin/analytics")
def analytics_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    summary = get_analytics_summary()
    transaction_data = get_transactions_by_type()
    account_data = get_accounts_by_type()
    recent_transactions = get_recent_transactions()
    top_accounts = get_top_account_balances()

    transaction_labels = [
        row[0] for row in transaction_data
    ]

    transaction_values = [
        row[1] for row in transaction_data
    ]

    account_labels = [
        row[0] for row in account_data
    ]

    account_values = [
        row[1] for row in account_data
    ]

    return render_template(
        "analytics_dashboard.html",
        summary=summary,
        transaction_labels=transaction_labels,
        transaction_values=transaction_values,
        account_labels=account_labels,
        account_values=account_values,
        recent_transactions=recent_transactions,
        top_accounts=top_accounts
    )
    
@app.route("/admin/users/<int:user_id>/financial-details")
def customer_financial_details(user_id):

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "error")
        return redirect(url_for("login_page"))

    customer_details, transactions = (
        get_customer_financial_details(user_id)
    )

    if customer_details is None:
        flash(
            "No customer account was found for this user.",
            "error"
        )
        return redirect(url_for("user_management_page"))

    return render_template(
        "customer_financial_details.html",
        customer_details=customer_details,
        transactions=transactions
    )

if __name__ == "__main__":
    create_tables()
    add_customer_id_to_users()
    add_role_to_users()
    app.run(debug=True)
    
