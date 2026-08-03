from user import User 
from database import create_tables, add_customer_id_to_users, add_role_to_users, insert_user

create_tables()
add_customer_id_to_users()
add_role_to_users()

admin = User(user_id=9001, username="admin",password="admin123",customer_id=None,role="Admin")

insert_user(admin)
print("Initial admin created")
