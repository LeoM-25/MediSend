def tables():
    import sqlite3

    with sqlite3.connect("MediSend.db")as db:
        cursor=db.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS A(
        ID INTEGER NOT NULL,
        Product TEXT PRIMARY KEY,
        Quantity INTEGER NOT NULL,
        Expiry Date TEXT NOT NULL);""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS B(
        ID INTEGER NOT NULL,
        Product TEXT PRIMARY KEY,
        Quantity INTEGER NOT NULL,
        Expiry Date TEXT NOT NULL);""")

    

