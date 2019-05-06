#!/usr/bin/python
import serial
import datetime
import sqlite3

# Serial port for edge device
ser = serial.Serial('/dev/ttyACM0', timeout = 0.5, write_timeout = 0.5)
ser.flushInput()

try:
	ser.write(b'A') # Write a character to the device
except:
	print("error")
	quit()

data = ser.read(100) # read back response
timestamp = datetime.datetime.now() # get the date and time

# Convert to string and get rid of newline and carriage return
data = str(data.decode('utf-8'))
data = data.rstrip()

data = data.split() #break up each data field

# Connect to sqlite database 
db = sqlite3.connect('/home/hgross/331/datalogger/database')
cursor = db.cursor()

# Insert data
cursor.execute('''INSERT INTO sensor_data(time,temp1, ir, fsi, vis, lux, temp2, pressure, humid) VALUES(?,?,?,?,?,?,?,?,?) ''', (timestamp, data[0], data[2], data[3], data[4], data[5], data[7], data[8], data[9]))

# Clean up anc close database
db.commit()
db.close()

