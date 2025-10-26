def request():
    import sqlite3

#Determines what tables are search add more to Tables to search others
#Order is a Place Holder
    Tables=["A","B"]
    Order=input("What is the barcode of the item you are requesting:")
    table_found=[]
    

    with sqlite3.connect("MediSend.db") as db:
        cursor=db.cursor()

#Searches the tables and store the tables which it is in
        for table in Tables:
            cursor.execute(f"SELECT 1 FROM {table} WHERE ID =?", (Order,))
            if cursor.fetchone():
                table_found.append(table)

#Prints the tables which the items are in if not print its not. Place Holder        
    if table_found:
        print(f"Your product is found in: {','.join(table_found)}")
    else:
        print("Sorry your product isn't availible somewhere else")
    
    
