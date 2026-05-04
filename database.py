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
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY,
            item_name TEXT,
            from_location TEXT,
            to_location TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Barcode_IDs(
            Barcode_ID INTEGER PRIMARY KEY,
            Product TEXT
        )
        """)

def find_item(barcode): # inputs barcode and outputs location + expiry
    locations = ["A", "B"]
    found = []

    product = get_product_from_barcode(barcode)

    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()

        for loc in locations:
            cursor.execute(
                f"SELECT Expiry_Date, Quantity FROM Pharmacy_{loc} WHERE ID = ?",
                (barcode,)
            )
            results = cursor.fetchall()

            for expiry, qty in results:
                found.append({
                    "product": product,
                    "location": f"Pharmacy_{loc}",
                    "expiry": expiry,
                    "quantity": qty
                })

    return found # inputs barcode and outputs location + expiry

# barcode

def get_product_from_barcode(barcode):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("SELECT Product FROM Barcode_IDs WHERE Barcode_ID=?", (barcode,))
        result = cursor.fetchone()
        return result[0] if result else None # only if there are any products

def get_waste_analysis():
    import sqlite3
    waste_count = {}

    today = datetime.now()

    with sqlite3.connect("MediSend.db") as db:
        cursor = db.cursor()

        for loc in ["A", "B"]:
            table = f"Pharmacy_{loc}"
            cursor.execute(f"SELECT Product, Expiry_Date, Quantity FROM {table}")
            rows = cursor.fetchall()

            for product, expiry, qty in rows:
                expiry_date = datetime.strptime(expiry, "%d/%m/%y")

                if expiry_date < today:
                    if product not in waste_count:
                        waste_count[product] = 0
                    waste_count[product] += qty

    # sort most wasted first
    sorted_waste = sorted(waste_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_waste

def add_barcode(barcode, product):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO Barcode_IDs (Barcode_ID, Product) VALUES (?, ?)",
            (barcode, product)
        )
        db.commit()

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
