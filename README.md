# Palestine Investment Bank - Banking System

A role-based banking system developed using **Python**, **Flask**, and **Supabase PostgreSQL** that simulates the core operations of a modern banking application.

---

# Overview

This project demonstrates object-oriented programming, web development, database management, authentication, authorization, and secure banking operations.

The application supports three different user roles:

- **Customer**
- **Teller**
- **Administrator**

Each role has its own dashboard, permissions, and banking operations, closely simulating how responsibilities are separated in a real banking environment.

---

# Features

## Customer

- Secure login
- View personal bank accounts
- View personal transaction history
- Deposit money into owned accounts
- Withdraw money from owned accounts
- Transfer money between accounts
- Loan calculator with monthly payment schedule
- Automatic logout support

---

## Teller

- Create customer accounts
- Deposit funds
- Withdraw funds
- Transfer money
- View all customer accounts
- View all transactions
- Loan calculator for customers

---

## Administrator

- Create Administrator accounts
- Create Teller accounts
- Manage all system users
- Activate and deactivate user accounts
- Automatic reactivation of locked accounts
- View customer financial details
- View all customer accounts
- View all banking transactions
- Analytics dashboard
- Monitor customer balances and transaction activity

---

# Security Features

- Password hashing using Werkzeug
- CSRF protection using Flask-WTF
- Secure session management
- Role-based access control
- Customer account ownership verification
- Automatic account deactivation after five failed login attempts
- Administrator account reactivation
- Protected database queries
- Environment variable configuration using `.env`

---

# Technologies Used

- Python
- Flask
- Supabase (PostgreSQL)
- HTML5
- CSS3
- Jinja2
- Flask-WTF
- Flask-Limiter
- Werkzeug

---

# Project Structure

```
PIB-Banking-System/
│
├── app.py
├── database.py
├── supabase_db.py
├── account.py
├── admin.py
├── teller.py
├── customer.py
├── customer_info.py
├── transactions.py
├── loan.py
├── helpers.py
├── seed_database.py
├── create_admin.py
├── requirements.txt
├── .gitignore
├── templates/
└── static/
```

---

# Authentication

The application uses secure role-based authentication.

After logging in, users are automatically redirected to their assigned dashboard.

- Customer Dashboard
- Teller Dashboard
- Administrator Dashboard

Unauthorized access is prevented through role verification and session validation.

---

# Database

The application uses **Supabase PostgreSQL** as the backend database.

The database stores:

- Users
- Customers
- Accounts
- Transactions
- Loan calculations
- Login security information

---

# Installation

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

Create a `.env` file and configure your Supabase credentials.

Example:

```env
SUPABASE_HOST=your_host
SUPABASE_DATABASE=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password
SUPABASE_PORT=5432
SECRET_KEY=your_secret_key
```

Run the application

```bash
python app.py
```

---

# Future Improvements

- Automatic account number generation
- Email notifications
- Two-factor authentication (2FA)
- PDF account statements
- Mobile banking interface
- Bill payment services
- Transaction search and filtering
- Multi-language support

---

# Author

**Nader Suleiman**

Computer Science Student

University of Puerto Rico Bayamón

GitHub:

https://github.com/Nader-Suleiman