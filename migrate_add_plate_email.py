"""
One-time migration: add car_plate and user_email columns to reservations table.
Run once: python migrate_add_plate_email.py
"""
import os
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'smart_parking'),
}

def column_exists(cursor, table, column):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = %s AND table_name = %s AND column_name = %s",
        (DB_CONFIG['database'], table, column)
    )
    return cursor.fetchone()[0] > 0

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()

    if not column_exists(cur, 'reservations', 'car_plate'):
        cur.execute("ALTER TABLE reservations ADD COLUMN car_plate VARCHAR(20) NULL AFTER user_name")
        print("  [+] Added column: car_plate")
    else:
        print("  [=] Column already exists: car_plate")

    if not column_exists(cur, 'reservations', 'user_email'):
        cur.execute("ALTER TABLE reservations ADD COLUMN user_email VARCHAR(255) NULL AFTER car_plate")
        print("  [+] Added column: user_email")
    else:
        print("  [=] Column already exists: user_email")

    conn.commit()
    print("\nMigration complete!")
except Error as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
