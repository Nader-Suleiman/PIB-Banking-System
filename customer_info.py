from datetime import datetime 

class CustomerInfo:
    
    def __init__(self, customer_id, full_name, phone, email, address):
        self.customer_id = customer_id
        self.full_name = full_name
        self.phone = phone 
        self.email = email 
        self.address = address 
        self.is_active = True 
        self.date_created = datetime.now()
        
        
    def display_info(self):
        print("Customer Information")
        print()
        print(f"Customer ID : {self.customer_id}")
        print(f"Full Name : {self.full_name}")
        print(f"Phone Number : {self.phone}")
        print(f"Address : {self.address}")
        print(f"Status : {'Active' if self.is_active else 'Inactive'}")
        print(f"created : {self.date_created.strftime('%Y-%m-%d %H:%M')}")

        print()
        
    def update_phone(self, new_phone):
        self.phone = new_phone 
        print("phone number updated successfully")
            
    def update_email(self,new_email):
        self.email = new_email
        print("email updated successfully")
            
    def update_address(self, new_address):
        self.address = new_address
        print("Address updated successfully")
        
    def deactivate(self):
        self.is_active = False 
        print("Customer has been deactivated")
            
    def activate(self):
        self.is_active = True 
        print("Customer has been activated")
            
        
