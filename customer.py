from user import User


class Customer(User):

    def __init__(self,user_id,username,password,customer_id,full_name,phone,email,address):
        super().__init__(user_id, username, password)

        self.customer_id = customer_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.address = address
        self.is_active = True

    def view_balance(self):
        print("Viewing account balance")

    def transfer_money(self):
        print("Transferring money")

    def view_transaction(self):
        print("Viewing transactions")