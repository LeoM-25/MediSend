def adding():
    import sqlite3
    from Tables import tables

    with sqlite3.connect("MediSend.db") as db:
     cursor = db.cursor()


    

    # Placeholder
    location = input("Please enter your location: ")
    item = input("Your item: ")
    barcode_data = int(input("Please scan your product: "))
    expiry=input("When does your item expire")

    #checks to see if database exists
    cursor.execute(f"SELECT * FROM  {location} WHERE ID=?",[barcode_data])
    result=cursor.fetchall()

    if result:
     cursor.execute(f"SELECT Expiry_Date FROM {location} WHERE ID={barcode_data}")
     for x in cursor.fetchall():
      if x[0]==expiry:
        cursor.execute(f"SELECT Quantity FROM {location} WHERE ID={barcode_data}")
        for x in cursor.fetchall():
            quantity=x
            quantity=int("".join(map(str, quantity)))
            quantity=quantity+1
            cursor.execute(f"UPDATE {location} SET Quantity=? WHERE ID=?",(quantity, barcode_data))
            db.commit()
      elif x[0]!=expiry:
        print("hi")
        quantity=1
        sql = f"INSERT INTO {location} (ID, Product, Quantity,Expiry_Date) VALUES (?,?,?,?)"
        cursor.execute(sql, (barcode_data, item, quantity, expiry))
        db.commit()
    else:
        print("hi")
        quantity=1
        sql = f"INSERT INTO {location} (ID, Product, Quantity,Expiry_Date) VALUES (?,?,?,?)"
        cursor.execute(sql, (barcode_data, item, quantity, expiry))
        db.commit()




