import sqlite3
from Adding_medicine import adding
from Tables import tables
from Requesting import request
from Delete import delete

with sqlite3.connect("MediSend.db") as db:
 cursor=db.cursor()

tables()

choice=int(input("Please choose one: \n 1) Adding Medicine \n 2) Requesting:"))

if choice==1:
    adding()
if choice==2:
    request()
if choice==3:
    delete()

    

