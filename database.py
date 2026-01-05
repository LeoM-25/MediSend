import sqlite3
# All Fin's original code as subprograms
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

def find_item(barcode): # inputs barcode and outputs location + expiry
    locations = ["A", "B"]
    found = []

    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()

        for loc in locations:
            cursor.execute(
                f"SELECT DISTINCT Expiry_Date FROM Pharmacy_{loc} WHERE ID = ?",
                (barcode,)
            )
            results = cursor.fetchall()

            for (expiry,) in results:
                found.append({"location": loc,"expiry": expiry})

    return found

