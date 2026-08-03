from datetime import datetime


class Transactions:
    transaction_counter = 1

    def __init__(
        self,
        account_number,
        transaction_type,
        amount,
        status="Successful"
    ):
        self.transaction_id = f"TXN{Transactions.transaction_counter:04d}"
        Transactions.transaction_counter += 1

        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.status = status
        self.date_created = datetime.now()

    def display_info(self):
        print("\nTransaction Information\n")
        print(f"Transaction ID : {self.transaction_id}")
        print(f"Account Number : {self.account_number}")
        print(f"Transaction Type : {self.transaction_type}")
        print(f"Amount : ${self.amount:.2f}")
        print(f"Status : {self.status}")
        print(
            f"Date : "
            f"{self.date_created.strftime('%Y-%m-%d %H:%M')}"
        )