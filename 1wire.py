import os
import glob
import time
import sqlite3
import sys

# creates a connection to the database
conn = sqlite3.connect("SensorData.db")
#Creates a cursor object, which allows interaction with the database and add
#data
cursor = conn.cursor()


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


#with conn:
for x in range(0, 10):
        Uread=read_temp()
        print(Uread)
        print("We're on time %d" % (x))
        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO onewire(name, data, date)VALUES ('webserver5', '%f', datetime())" % (Uread)
        cursor.execute(sql)
        conn.commit()
        time.sleep(3)

    #cursor.execute("SELECT * FROM onewire")
    #rows = cursor.fetchall()

    #for row in rows:
    #    print (row)
