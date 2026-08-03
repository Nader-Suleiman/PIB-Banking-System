class Loan: 
    
    def __init__(self, loan_id, customer_id, principal, annual_interest_rate, loan_term_months):
        
        self.loan_id = loan_id
        self.customer_id = customer_id 
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.loan_term_months = loan_term_months
        self.remaining_balance = principal
        self.is_active = True 
        self.monthly_installment = self.calculate_monthly_installment() 
        
    def calculate_monthly_installment(self):
        monthly_interest_rate = (self.annual_interest_rate / 100 ) / 12 
        
        if monthly_interest_rate == 0:
            return self.principal / self.loan_term_months
        
        installment = (self.principal * monthly_interest_rate * (1 + monthly_interest_rate) ** self.loan_term_months) / ((1 + monthly_interest_rate) ** self.loan_term_months - 1)
        
        return installment 
    
    def display_info(self):
        print("\nLoan Information")
        print()
        print(f"Loan ID : {self.loan_id}")
        print(f"Customer ID : {self.customer_id}")
        print(f"principal : ${self.principal:.2f}")
        print(f"Annual Interest Rate : {self.annual_interest_rate:.2f}%")
        print(f"Loan Term Months : {self.loan_term_months}")
        print(f"Monthly Installments :" f"${self.monthly_installment:.2f}")
        print("Remaining Balance:" f"${self.remaining_balance:.2f}")
        print(f"Status: " f"{'Active' if self.is_active else 'Paid'}")
        
    
    def make_payment(self):

        if not self.is_active:
            print("Loan has already been paid.")
            return
        amount = self.monthly_installment

        if amount <= 0:
            print("Error: Payment must be greater than 0.")
            return

        monthly_interest_rate = (
            self.annual_interest_rate / 100) / 12

        interest_amount = (
            self.remaining_balance * monthly_interest_rate)

        principal_amount = amount - interest_amount

        if principal_amount <= 0:
            print("Error: Payment is not enough to cover the interest.")
            return

        if principal_amount >= self.remaining_balance:
            principal_amount = self.remaining_balance
            amount = principal_amount + interest_amount
            

        self.remaining_balance -= principal_amount
        
        if self.remaining_balance <= 0:
            self.remaining_balance = 0
            self.is_active = False

        print("\nPayment received successfully.")
        print(f"Payment amount: ${amount:,.2f}")
        print(f"Interest paid: ${interest_amount:,.2f}")
        print(f"Principal paid: ${principal_amount:,.2f}")
        print(f"Remaining balance: ${self.remaining_balance:,.2f}")

        if not self.is_active:
            print("Loan has been fully paid.")
            
    def generate_payment_schedule(self):
        
        temporary_balance = self.remaining_balance
        
        monthly_interest_rate = (self.annual_interest_rate / 100) / 12 
        
        print("\n" + "=" * 85)
        print("LOAN PAYMENT SCHEDULE")
        print("=" * 85)
        
        print(
            f"{'payment':<10}"
            f"{'Starting Balance' :<20}"
            f"{'Payment Amount' :<18}"
            f"{'Interest' :<15}"
            f"{'Principal' :<15}"
            f"{'Remaining Balance' :<20}")
        
        print ("-" * 85)
        
        for payment_number in range (1, self.loan_term_months + 1): 
            starting_balance = temporary_balance
            interest_amount = (starting_balance * monthly_interest_rate)
            
            payment_amount = self.monthly_installment
            principal_amount = (payment_amount - interest_amount)
            
            if principal_amount > temporary_balance:
                principal_amount = temporary_balance
                payment_amount = (principal_amount + interest_amount)
            
            temporary_balance -= principal_amount
            
            if temporary_balance < 0: 
                temporary_balance = 0 
                
            print(
                f"{payment_number:<10}"
                f"${starting_balance:<19,.2f}"
                f"${payment_amount:<17,.2f}"
                f"${interest_amount:<14,.2f}"
                f"${principal_amount:<14,.2f}"
                f"${temporary_balance:<19,.2f}"
            )
            
        print("-" * 85 )
        
    def get_payment_schedule(self):
        schedule = []

        temporary_balance = self.remaining_balance

        monthly_interest_rate = (
            self.annual_interest_rate / 100
        ) / 12

        for payment_number in range(1, self.loan_term_months + 1):

            starting_balance = temporary_balance

            interest_amount = (
                starting_balance * monthly_interest_rate
            )

            payment_amount = self.monthly_installment

            principal_amount = (
                payment_amount - interest_amount
            )

            if principal_amount > temporary_balance:
                principal_amount = temporary_balance
                payment_amount = principal_amount + interest_amount

            temporary_balance -= principal_amount

            if temporary_balance < 0:
                temporary_balance = 0

            schedule.append({
                "payment_number": payment_number,
                "starting_balance": starting_balance,
                "payment_amount": payment_amount,
                "interest_amount": interest_amount,
                "principal_amount": principal_amount,
                "remaining_balance": temporary_balance
            })

            if temporary_balance == 0:
                break

        return schedule
        
        