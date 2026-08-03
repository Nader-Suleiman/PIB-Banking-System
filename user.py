
class User: 
    
    def __init__(self, user_id, username, password, customer_id=None, role="Customer" ):
        self.user_id = user_id 
        self.username = username 
        self.password = password 
        self.customer_id = customer_id
        self.role = role
        self.is_active =  True 
        
    def display_info(self):
        print(f"User ID: {self.user_id}")
        print(f"Username: {self.username}")
        print(f"Customer ID: {self.customer_id}")
        print(f"Role: {self.role}")
        print(f"Status: {'Active' if self.is_active else 'Inactive'}")
        
              
              
        
        
        
        
    