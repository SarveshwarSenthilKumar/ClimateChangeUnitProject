
from flask import Flask, render_template, request, redirect, session
from flask_session import Session 
import os
import sqlite3
from sql import *
import os

app = Flask(__name__)

@app.route("/comparison")
def index():
  db = SQL("sqlite:///cars.db")
  results=db.execute("SELECT * FROM cars")
  return render_template("index.html", results=results)

@app.route("/", methods=["GET", "POST"])
def intro():
  return render_template("intro.html")

@app.route("/results", methods=["GET", "POST"])
def results():
  car1 = request.form.get("car1")
  car2 = request.form.get("car2")

  print(car2)

  db = SQL("sqlite:///cars.db")
  
  car1results = db.execute("SELECT * FROM cars WHERE id = :id", id=car1)[0]
  car2results = db.execute("SELECT * FROM cars WHERE id = :id", id=car2)[0]

  moneySavedPerYear = 0
  moneySavedPerLifetime = 0
  CO2ReducedPerYear = 0
  CO2ReducedPerLifetime = 0

  car1ge = car1results["gasMileage"]
  car2ge = car2results["gasMileage"]

  difference = float(car1ge) - float(car2ge)

  averageGasPrice = 172.7
  #Average as of October 31, 2022

  moneySavedPerYear = (difference*averageGasPrice)*153
  moneySavedPerYear = round(moneySavedPerYear/100, 2)

  moneySavedPerLifetime = round(moneySavedPerYear*12, 2)

  CO2perLitre = 2.3

  CO2ReducedPerYear = round((difference*CO2perLitre)*153, 2)

  CO2ReducedPerLifetime = round(CO2ReducedPerYear*12, 2)

  cars=[car1results, car2results]
  
  return render_template("results.html", cars=cars, CO2perLitre=CO2perLitre, averageGasPrice=averageGasPrice, moneySavedPerYear=str(moneySavedPerYear), moneySavedPerLifetime=str(moneySavedPerLifetime), CO2ReducedPerYear=str(CO2ReducedPerYear), CO2ReducedPerLifetime=str(CO2ReducedPerLifetime))

@app.route("/upload", methods=["GET", "POST"])
def upload():
  if request.method == "GET":
    return render_template("uploadcar.html")
  elif request.method == "POST":
    vehicleName = request.form.get("vehicleName")
    pictureLink = request.form.get("pictureLink")
    gasMileage = request.form.get("gasMileage")
    numberSold = request.form.get("numberSold")
    vehicleType = request.form.get("vehicleType")
    seats = request.form.get("seats")
    password = request.form.get("password")
    
    if password == os.getenv('PASS'):
      db = SQL("sqlite:///cars.db")
      db.execute("INSERT INTO cars (vehicleName, pictureLink, gasMileage, numberSold, vehicleType, seats) VALUES(?,?,?,?,?,?)", vehicleName, pictureLink, gasMileage, numberSold, vehicleType, seats)

      return render_template("sentence.html", sentence="The car has been uploaded!")
    return render_template("sentence.html", sentence="The password is incorrect!")

@app.route("/check")
def check():
  db=SQL("sqlite:///cars.db")
  results = db.execute("SELECT * FROM cars")
  return results

app.run(host='0.0.0.0', port=8000)