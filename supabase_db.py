import os

import psycopg
from dotenv import load_dotenv


load_dotenv(override=True)


def get_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing from the .env file."
        )

    return psycopg.connect(
        database_url,
        prepare_threshold=None
    )
    
def get_all_users_supabase():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                user_id,
                username,
                role,
                is_active,
                customer_id
            FROM users
            ORDER BY user_id
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
    