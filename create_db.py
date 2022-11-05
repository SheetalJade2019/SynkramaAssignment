# importing required libraries
import mysql.connector
# download & install mysql database add here user & password 
# https://www.geeksforgeeks.org/python-mysql-create-database/

dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="root"
)
 
# preparing a cursor object
cursorObject = dataBase.cursor()
 
# creating database
cursorObject.execute("CREATE DATABASE synkrama")