def create_tables():
    import sqlite3

    with sqlite3.connect("MediSend.db")as db:
        cursor=db.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pharmacy_A(
        ID INTEGER NOT NULL,
        Product TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        Expiry_Date TEXT NOT NULL);""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pharmacy_B(
        ID INTEGER NOT NULL,
        Product TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        Expiry_Date TEXT NOT NULL);""")
