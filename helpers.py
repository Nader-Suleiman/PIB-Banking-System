from flask import session

def login_required():
    return "user_id" in session

def is_customer():
    return session.get("role") == "customer"

def is_teller():
    return session.get("role") == "teller"

def is_admin():
    return session.get("role") == "admin"

def is_staff():
    return session.get("role") == ["admin" , "teller"]
