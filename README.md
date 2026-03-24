# Welcome to MediSend!
MediSend is our system for logging and sharing medicine, designed to reduce wastage and improve access to medicine in places where medicine supplies are limited. This is our submission for the PA Raspberry Pi compettion 2026.
# Running MediSend
To run, main.py, database.py, imports.py and medisend.db must be downloaded. The package Kivy is needed in order to run the UI. On the raspberry pi, if all the files are in the same directory, python3 main.py should launch the program. If not, then the database may not be created and so you will need to run the subprogram make_tables() in database.py seperately.
