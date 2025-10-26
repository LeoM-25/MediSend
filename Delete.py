def delete():
    import sqlite3

    with sqlite3.connect("MediSend.db") as db:
     cursor = db.cursor()

    tables=["A", "B"]

    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        db.commit()
