# 🏦 Palestine Investment Bank - Banking System

A role-based banking system developed using **Python**, **Flask**, and **SQLite** that simulates the core operations of a modern banking application.

---

## Overview

This project was designed to demonstrate object-oriented programming, database management, user authentication, and role-based access control.

The system supports three different user roles:

- **Customer**
- **Teller**
- **Administrator**

Each role has its own dashboard and permissions, closely simulating how real banking systems separate responsibilities.

---

## Features

### Customer
- Secure login
- View personal bank accounts
- View transaction history
- Deposit money
- Withdraw money
- Transfer funds
- Apply for loans

---

### Teller
- Create customer accounts
- Deposit funds
- Withdraw funds
- Transfer money
- Create loans for customers

---

### Administrator
- Create Teller accounts
- Create Administrator accounts
- Manage system users
- Activate and deactivate users
- View all customer accounts
- View all banking transactions

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2

---

## Project Structure

```
PIB-Banking-System/
│
├── app.py
├── database.py
├── account.py
├── customer.py
├── loan.py
├── user.py
├── helpers.py
├── requirements.txt
├── templates/
└── static/
```

---

## Authentication

The application uses role-based authentication.

After logging in, users are automatically redirected to the correct dashboard based on their role.

- Customer Dashboard
- Teller Dashboard
- Administrator Dashboard

Access to protected pages is restricted according to user permissions.

---

##  Database

The application uses **SQLite** to store:

- Users
- Customers
- Accounts
- Transactions
- Loans

---

##  Installation

Clone the repository

```bash
git clone https://github.com/Nader-Suleiman/PIB-Banking-System.git
```

Move into the project

```bash
cd PIB-Banking-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

## Future Improvements

- Automatic account number generation
- Password hashing
- Email notifications
- Interest calculations
- Mobile responsive design
- Two-factor authentication
- Account statements (PDF)

---

## Author

**Nader Suleiman**

Computer Science Student  
University of Puerto Rico Bayamon

GitHub:
https://github.com/Nader-Suleiman