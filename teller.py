from user import User 

class Teller(User):
    
    def __init__(self, user_id, username, password):
            super().__init__(user_id, username, password)
            
    def create_customer(self):
        print("Creating new customer")
        
    def process_transactions(self):
        print("Processing transactions")
        