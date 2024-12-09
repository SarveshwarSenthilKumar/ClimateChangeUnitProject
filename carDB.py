import sqlite3
import os

os.remove("cars.db")
connection = sqlite3.connect("cars.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE cars (id INTEGER, vehicleName, pictureLink, gasMileage, numberSold, vehicleType, seats, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("cars.db", "r")
test.close()