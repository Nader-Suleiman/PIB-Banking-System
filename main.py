from admin import Admin 
from user import User 
from teller import Teller 
from customer import Customer
from customer_info import CustomerInfo
from account import Account 
from transactions import Transactions
from loan import Loan
from database import create_tables, insert_customer, view_customers, insert_account, view_accounts, insert_transaction, view_transaction, update_account_balance, insert_loan, update_loan_balance, view_loans


print("=" * 50)
print("DATABASE SETUP")
print("=" * 50)

create_tables()
print()

admin = Admin(1234, "Nader Mehirz", "admin1234")
teller = Teller(1235, "Omar Nader", "teller1235")
customeruser = Customer(1236, "Mohammad Mehriz", "customeruser1236")
customer_record = CustomerInfo(1001, "Mehriz Suleiman", "0591231234", "nsma@gmail.com", "Ramallah")
customer_record2 = CustomerInfo(1002,"Second Customer","0590000000","customer2@gmail.com","Nablus")
insert_customer(customer_record)
insert_customer(customer_record2)

view_customers()

print("Admin Information")
admin.display_info()
admin.create_user()
admin.view_report()

print()


print("Teller Information")
teller.display_info()
teller.create_customer()
teller.process_transactions()


print()

print("Customer Information")
customeruser.display_info()
customeruser.view_balance()
customeruser.transfer_money()
customeruser.view_transaction()

print()

customer_record.display_info()


print("\nUpdating customer information...\n")
customer_record.update_phone("0592432342")
customer_record.update_email("ahmad.ali@email.com")
customer_record.update_address("Nablus")

customer_record.display_info()


print("\nDeactivating customer...\n")

customer_record.deactivate()
customer_record.display_info()


print("\nActivating customer again...\n")

customer_record.activate()
customer_record.display_info()

print() 

account_record = Account("ACC1001", 1001, "Savings", 500.00)
account2= Account("ACC1002", 1002, "savings", 1000)
insert_account(account_record)
insert_account(account2)
view_accounts()

account_record.display_info()

print() 

print("===========================DEPOSIT===========================================")

amount = float(input("How much would you like to deposit: "))

account_record.deposit(amount)
insert_transaction(account_record.transactions[-1])
update_account_balance(account_record)

view_transaction()

print()
account_record.display_info()

print() 
print("==========================WITHDRAW===========================================")

amount = float(input("Enter the amount you would like to withdraw: "))
previous_transaction_count = len(account_record.transactions)
account_record.withdraw(amount)

if len(account_record.transactions) > previous_transaction_count:
    insert_transaction(account_record.transactions[-1])
    update_account_balance(account_record)

print()
account_record.display_info()
print()

print("===========================TRANSFER============================================")

account1 = account_record

account1.display_info()
account2.display_info()

print()

amount = float(input("Enter the amount of money you would like to transfer: "))

account1_previous_count = len(account1.transactions)
account2_previous_count = len(account2.transactions) 

account1.transfer(account2,amount)

if (len(account1.transactions) > account1_previous_count and len(account2.transactions) > account2_previous_count):
    # Save Transfer Out transaction
    insert_transaction(account1.transactions[-1])

    # Save Transfer In transaction
    insert_transaction(account2.transactions[-1])

    # Update both balances in the database
    update_account_balance(account1)
    update_account_balance(account2)

account1.display_info()
account2.display_info()

print()


account1.display_transactions()

account2.display_transactions()

print()
view_accounts()
view_transaction()

print("========================================LOAN======================================")

loan1 = Loan("LN1001", 1001, 10000, 6, 24)
insert_loan(loan1)

loan1.display_info()

print()

loan1.generate_payment_schedule()

print()

loan1.make_payment()
update_loan_balance(loan1)

print()

loan1.display_info()

print()
view_loans()

 

