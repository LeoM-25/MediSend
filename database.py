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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Barcode_IDs(
                ID INTEGER, 
                Product TEXT, 
                Barcode_ID INTEGER
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

# from the adding_medicine file

def add(data_to_add):
    import sqlite3
    # data_to_add = [item_name, expiry_date, quantity, dosage, location, barcode]

    with sqlite3.connect("MediSend.db") as db:
        cursor = db.cursor()
        # takes from list
        location = data_to_add[4]
        item = data_to_add[0]
        # dosage = data_to_add[3]
        barcode_data = data_to_add[5]

        expiry = data_to_add[1]

        # Check if the item exists in the table
        cursor.execute(f"SELECT Expiry_Date, Quantity FROM {location} WHERE ID=?", (barcode_data,))
        results = cursor.fetchall()

        if results:
            updated = False
            for exp_date, qty in results:
                if exp_date == expiry:
                    # update quantity
                    new_qty = qty + 1
                    cursor.execute(
                        f"UPDATE {location} SET Quantity=? WHERE ID=? AND Expiry_Date=?",
                        (new_qty, barcode_data, expiry)
                    )
                    db.commit()
                    updated = True
                    break
            if not updated:
                cursor.execute(
                    f"INSERT INTO {location} (ID, Product, Quantity,  Expiry_Date) VALUES (?, ?, ?, ?)",
                    (barcode_data, item, 1, expiry)
                )
                db.commit()
        else:
            cursor.execute(f"INSERT INTO {location} (ID, Product, Quantity, Expiry_Date) VALUES (?, ?, ?, ?)",(barcode_data, item, 1, expiry))
            db.commit()
