'''
Created by alfredc333
First Cypress Limited, 2014
MIT license
'''

import subprocess
import re
import sys
import time
import datetime
import serial
from Adafruit.Adafruit_BMP085 import BMP085
from time import strftime
import RPi.GPIO as GPIO
import smbus
import time
import os
from time import gmtime, strftime, localtime

import sqlite3

import logging
import logging.config

import ConfigParser

import lcd16x2lib

# define 3 CO2 content levels
class alarmStatus:
  Green, Yellow, Red = range(0, 3)

# Read parameters from configuration file
config = ConfigParser.ConfigParser()
config.read("./liv.config")

thSensorOn = config.getboolean('ON_BOARD_SENSORS', 'temp_humidity_sensor')
apSensorOn = config.getboolean('ON_BOARD_SENSORS', 'air_pressure_sensor')
co2SensorOn = config.getboolean('ON_BOARD_SENSORS', 'co2_sensor')
useDBOn = config.getboolean('SQLITE_DB', 'useDB')

apAddress = config.get('AIR_PRESSURE_SENSOR', 'I2C_address')

thType = config.get('TEMP_HUMIDITY_SENSOR', 'type')
thGPIO = config.get('TEMP_HUMIDITY_SENSOR', 'gpio_no')

CO2_ALARM_1 = config.getint('CO2_SENSOR', 'co2_alarm_1')
CO2_ALARM_2 = config.getint('CO2_SENSOR', 'co2_alarm_2')

LCDAddress = config.get('LCD_DISPLAY', 'I2C_address')
LCDPort = config.getint('LCD_DISPLAY', 'port_no')


#logging.basicConfig(filename='liv.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

logger.info('--------------------------------------------')
logger.info('LIV STARTED')


# os.environ ['TZ'] = 'Asia / Hong_Kong'
# time.tzset ()


# init co2 sensor if present

co2AlarmStatus = alarmStatus.Green

temperatureString = "NO TEMP SENSOR";
humidityString = "NO HUM SENSOR";
airPressureString = "NO AP SENSOR";
co2String = "NO CO2 SENSOR";

# LCD init code 
lcd = lcd16x2lib.lcd16x2(int(LCDAddress, 16), LCDPort)
lcd.initDisplay()
logger.info('LCD initialized')

# Initialize airPressure sensor if present
# BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True). SAME CODE works for BMP180
if (apSensorOn):
  bmp = BMP085(int(apAddress, 16))
  airPressureString = "AP READ ERROR";
  logger.info('air pressure sensor initialized')
 
# initialize serial connection with CO2 sensor if present
if (co2SensorOn):
  ser = serial.Serial("/dev/ttyAMA0")
  co2String = "CO2 READ ERROR";
  logger.info('CO2 sensor serial port connected')
  ser.flushInput()
  time.sleep(1)

# initialize db connection 
# conect to sqlite DB
if (useDBOn):
  dbconn = sqlite3.connect('liv.db')
  c = dbconn.cursor()
  logger.info('sqlite DB Connection initialized')


# keep trying to get a reading from DHT22 sensor for max 10 times 
if (thSensorOn):
  temperatureString = "TEMP READ ERROR";
  humidityString = "HUM READ ERROR";
  logger.info('temperature sensor initialized')
 
while(True):
  if (thSensorOn): 
    temperatureString = '-999'
    humidityString    = '-999'
    i = 1
    while (i < 11):
      try:
        subprocess.Popen(["./timer.sh"]);
        logger.info('timer started in livDemo process')
        logger.info('start Adafruit process')
        output = "EMPTY STRING"
        output = subprocess.check_output(["./Adafruit/Adafruit_DHT", thType, thGPIO]);
      except:
        # print "Unexpected error:", sys.exc_info()[0]
        logger.info("Unexpected error! " + str(sys.exc_info()[0]))
        # raise
        # print output
      matches = re.search("Temp =\s+([0-9.]+)", output)
      if (not matches):
        logger.info('temp NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      temp = float(matches.group(1))
      temperatureString = str(temp)

      # search for humidity printout
      matches = re.search("Hum =\s+([0-9.]+)", output)
      if (not matches):
        logger.info('humidity NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      humidity = float(matches.group(1))
      humidityString = str(humidity)
      logger.debug("Temp and Humidity sensor read after  " + str(i) + " tries")  
      break 

    if (i == 11):
      logger.debug("Faied to read Temp and Humidity after  " + str(i) + " tries")  

  # use temperature reading from DHT22 not BMP85/BMP180 since DHT22 is more accurate
  # temp = bmp.readTemperature()
  # pressure = bmp.readPressure()
  # altitude = bmp.readAltitude()
  if (apSensorOn):
    pressure = bmp.readPressure()
    airPressure = pressure / 100.0
    airPressureString = str(airPressure)
    
  if (co2SensorOn):
    # read K30 CO2 from serial 
    ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.01)
    resp = ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    co2 = (high * 256) + low
    co2String = str(co2)
   # set alarm status 
   
    if co2 < CO2_ALARM_1:
      if (co2AlarmStatus == alarmStatus.Red or co2AlarmStatus == alarmStatus.Yellow) :
        co2AlarmStatus = alarmStatus.Green
    elif co2 < CO2_ALARM_2:
      if (co2AlarmStatus == alarmStatus.Green or co2AlarmStatus == alarmStatus.Red) :
        co2AlarmStatus = alarmStatus.Yellow
    else:
      if (co2AlarmStatus == alarmStatus.Green or co2AlarmStatus == alarmStatus.Yellow) :
        co2AlarmStatus = alarmStatus.Red   
   
  logger.debug("AirPressure:  " + airPressureString) 
  logger.debug("Temperature:  " + temperatureString)
  logger.debug("Humidity:     " + humidityString)
  logger.debug("CO2 = " + co2String)
  
  # time stamp for future connected appliances reporting. will need to use network time  
  timestamp = strftime("%Y-%m-%d %H:%M:%S")
 
  # WRITE RECORD IN THE DB HERE
  # 'INSERT INTO Measurements VALUES(null ,\'2014-01-28 10:37:09\', 21.5, 76.9, 1200, 650)')
  if (useDBOn):
    if (not(apSensorOn)):
      DBairPressureString = "-999"
    else:
      DBairPressureString = airPressureString 
    if (not(thSensorOn)):
      DBtemperatureString = "-999"
      DBhumidityString = "-999"
    else:
      DBtemperatureString = temperatureString
      DBhumidityString = humidityString
    if (not(co2SensorOn)):
      DBco2String = "-999"
    else:
      DBco2String = co2String          
   
    logger.info("Inserting record into firstCypress Measurements table:") 
    dbstring = "INSERT INTO Measurements VALUES (null, '" + str(timestamp) + "', " + \
        DBtemperatureString + ", " + DBhumidityString + ", " + DBairPressureString + ", " + DBco2String + ")" 
    c.execute(dbstring)
    dbconn.commit()  
    logger.info(dbstring) 
     
  # LCD control code needs improvement
  
  for repeatDisplay in range(0, 3):
   
    for displayCounter in range(0, 4):
      if displayCounter == 0:
        line1 = "Air Pressure"
        line2 = airPressureString + " hPa"
      if displayCounter == 1:
        # if you live in North America, you probably use Fahrenheit
        # you can u translate C to F if you want
        line1 = "Temperature"
        line2 = temperatureString + " C"
      if displayCounter == 2:
        line1 = "Humidity"
        line2 = humidityString + " %"
      if displayCounter == 3:
        line1 = "CO2 Level"
        line2 = co2String + " ppm"
      
      # First line first column
      lcd.cleanFirstLine()        
      # Second line first column
      lcd.cleanSecondLine()    
      time.sleep(2)
      # First line first column
      lcd.writeFirstLine(line1)     
      # Second line first column
      # blink every 2 sec if yellow, blink every 1 sec if red
      # CO2 display cycle 10 sec, everything else 5sec
      if displayCounter == 3:
        if co2AlarmStatus == alarmStatus.Yellow:
          for x in range(0, 5):
            lcd.writeSecondLine(line2)
            time.sleep(2)
            lcd.cleanSecondLine()
            time.sleep(2)        
        elif co2AlarmStatus == alarmStatus.Red:
          for x in range(0, 10):
            lcd.writeSecondLine(line2)
            time.sleep(1)
            lcd.cleanSecondLine()
            time.sleep(1)
        else:
          lcd.writeSecondLine(line2)
          time.sleep(10)
        logger.info("Finished display cycle " + str(repeatDisplay))
      
      else:  
        lcd.writeSecondLine(line2)
        time.sleep(5)
               
