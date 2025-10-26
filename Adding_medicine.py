def adding():
    import sqlite3

    with sqlite3.connect("MediSend.db") as db:
     cursor = db.cursor()


    cursor.execute("""
         CREATE TABLE IF NOT EXISTS A(
                ID INTEGER NOT NULL,
                Product TEXT PRIMARY KEY,
                Quantity INTEGER NOT NULL);""")

    # Placeholder
    location = input("Please enter your location: ")
    item = input("Your item: ")
    barcode_data = int(input("Please scan your product: "))

    #checks to see if database exists
    cursor.execute(f"SELECT * FROM  {location} WHERE ID=?",[barcode_data])
    result=cursor.fetchall()
    if result:
        cursor.execute(f"SELECT Quantity FROM {location} WHERE ID={barcode_data}")
        for x in cursor.fetchall():
            quantity=x
            quantity=int("".join(map(str, quantity)))
            quantity=quantity+1
            cursor.execute(f"UPDATE {location} SET Quantity=? WHERE ID=?",(quantity, barcode_data))
            db.commit()
    else:
        quantity=1
        sql = f"INSERT INTO {location} (ID, Product, Quantity) VALUES (?, ?, ?)"
        cursor.execute(sql, (barcode_data, item, quantity))
        db.commit()


