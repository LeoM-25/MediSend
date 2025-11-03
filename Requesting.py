def request():
    import sqlite3

    Tables = ["A", "B"]
    Order = int(input("What is the barcode of the item you are requesting:"))
    table_found = []

    with sqlite3.connect("MediSend.db") as db:
        cursor = db.cursor()

        for table in Tables:
            cursor.execute(f"SELECT DISTINCT Expiry_Date FROM {table} WHERE ID = ?", (Order,))
            results = cursor.fetchall()

            for row in results:
                expiry = row[0]
                table_found.append(f"{table} {expiry}")

    if table_found:
        print(f"Your product is found in: {', '.join(table_found)}")
    else:
        print("Sorry, your product isn't available somewhere else.")
