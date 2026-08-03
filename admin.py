from user import User

class Admin(User):
    
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)
        
    def create_user(self):
        print("creating new user")
        
    def view_report(self):
        print("Viewing report")
         

