import sqlite3

DB_NAME = "MediSend.db" # In case we change the name of the DB

def create_tables():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pharmacy_A(
                ID INTEGER, 
                Product TEXT, 
                Quantity INTEGER, 
                Expiry_Date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pharmacy_B(
                ID INTEGER, 
                Product TEXT, 
                Quantity INTEGER, 
                Expiry_Date TEXT
            )
        """)
