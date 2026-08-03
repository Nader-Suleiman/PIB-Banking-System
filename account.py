from transactions import Transactions
class Account: 
    
    def __init__(self, account_number, customer_id, account_type, balance=0.0):
        
        self.account_number = account_number 
        self.customer_id = customer_id
        self.account_type = account_type    
        self.balance = balance 
        self.is_active = True 
        
        self.transactions = []
        
    def display_info(self):
        print("Account Information")
        print()
        print(f"Account Number : {self.account_number}")
        print(f"Customer ID : {self.customer_id}")
        print(f"Account type : {self.account_type}")
        print(f"Balance : {self.balance:.2f}")
        print(f"Status : " f"{'Active' if self.is_active else 'Inactive'}")
        print()
        
    
    def deposit(self, amount): 
        if not self.is_active: 
            print("Error, Account not active")
            return 
        if amount <= 0: 
            print("Error, deposit amount must be greater than 0")
            return 
            
        self.balance += amount
        self.record_transaction("Deposit", amount, "Successful")
        print() 
        print("Money deposited successfully")

    
    def withdraw(self, amount):
        if not self.is_active: 
            print("Error, Account not active")
            return 
        if amount <= 0: 
            print("Error, The amount must be greater than 0")
            return
        if amount > self.balance:
            print("Error, Insufficient funds")
            return 
        
        self.balance -= amount
        self.record_transaction("Withdrawal", amount, "Successful") 
        
        print("Withdrawal successful")
        print(f"withdrawn amount: $ {amount:.2f}")
        print(f"remaining balance is: {self.balance:.2f}")
        
        
    def transfer(self, receiver_account, amount):
        if not self.is_active:
            print("Error account not active") 
            return 
        if not receiver_account.is_active: 
            print("Error, receiver account is not active")
            return 
        
        if amount <= 0: 
            print("Error, Transfer amount must be greater than 0")
            return 
        
        if amount > self.balance:
            print("Not enough funds")
            return 
        
        self.balance -= amount
        receiver_account.balance += amount

        self.record_transaction("Transfer Out", amount,"Successful")

        receiver_account.record_transaction("Transfer In",amount,"Successful")

        print("Transfer completed successfully.")
        
    def deactivate(self):
        self.is_active = False
        print("Account has been deactivated")
        
    def activate(self):
        self.is_active = True 
        print("Account has been activated")
        
    def record_transaction(self, transaction_type, amount, status):
        transaction = Transactions(
        self.account_number,
        transaction_type,
        amount,
        status
        )

        self.transactions.append(transaction)
        
    def display_transactions(self):
        print("\nTransaction History")
        print()
        if len(self.transactions) == 0:
            print("No transactions found.")
            return

        for transaction in self.transactions:
            transaction.display_info()

        
            
        
                                
        
        
    