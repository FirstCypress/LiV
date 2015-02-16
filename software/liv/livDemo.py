'''
Created on August 27, 2014 by alfredc333

'''

import subprocess
import re
import sys
import time
from time import gmtime, strftime, localtime
import datetime
import serial
import os
import sqlite3
import logging
import logging.config
import ConfigParser
import smbus
import RPi.GPIO as GPIO
from Adafruit_Python_BMP.Adafruit_BMP import BMP085
from lcd16x2 import lcd16x2
from co2Sensor import co2Sensor 
from airPressureSensor import airPressureSensor
from temperatureHumiditySensor import temperatureHumiditySensor

# define 3 CO2 content levels
class alarmStatus:
  Green, Yellow, Red = range(0, 3)

# Read parameters from configuration file
config = ConfigParser.ConfigParser()
config.read('./liv.config')

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

#set initial co2 alarm status 
co2AlarmStatus = alarmStatus.Green

temperatureString = 'NO TEMP SENSOR';
humidityString = 'NO HUM SENSOR';
airPressureString = 'NO AP SENSOR';
co2String = 'NO CO2 SENSOR';

# LCD init code 
lcd = lcd16x2(int(LCDAddress, 16), LCDPort)
lcd.initDisplay()
logger.info('LCD initialized')

# Initialize airPressure sensor if present
# BMP085 and use HIGH RESOLUTION mode
if (apSensorOn):
  try:
    airPressureString = "ERROR";
    bmp = airPressureSensor(3, int(apAddress, 16))
    logger.info('Air pressure sensor initialized')
  except:
    logger.error('Air pressure sensor failed to initialize')
    
# initialize CO2 sensor if present
if (co2SensorOn):
  try:
    co2String = 'ERROR'
    co2s = co2Sensor()
    logger.info('co2 sensor initialized')
  except:
    logger.error('co2 sensor failed to initialize')
    
# initialize temp and humidity sensor if present
if (thSensorOn):
  try:
    temperatureString = 'ERROR';
    humidityString = 'ERROR';
    ts = temperatureHumiditySensor(thType, thGPIO, logger)
    logger.info('Temp and Humidity sensor initialized')
  except:
    logger.error('Temp and Humidity sensor failed to initialize')
    
    
# initialize db connection 
# conect to sqlite DB
if (useDBOn):
  try:
    dbconn = sqlite3.connect('liv.db')
    c = dbconn.cursor()
    logger.info('sqlite DB Connection initialized')
  except:
    logger.error('sqlite DB Failed to initialize')
    
    
  while(True):
    if(thSensorOn):
      temperatureString, humidityString = ts.readTemperatureHumidity()   

    if (apSensorOn):
      try:
        pressure = bmp.readAirPressure()
        airPressureString = str(pressure)
      except:
        airPressureString = 'ERROR'
        logger.error('Failed to read air pressure sensor')

    if (co2SensorOn):
      try:
        co2 = co2s.readCO2Level()
        co2String = str(co2)
      except:
        co2String = 'ERROR'
        logger.error('Failed to read co2 sensor')

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
   
    logger.info("AirPressure:  " + airPressureString) 
    logger.info("Temperature:  " + temperatureString)
    logger.info("Humidity:     " + humidityString)
    logger.info("CO2 = " + co2String)
 
    #time stamp for future connected appliances reporting. will need to use network time  
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
 
    # WRITE RECORD IN THE DB HERE
    # 'INSERT INTO Measurements VALUES(null ,\'2014-01-28 10:37:09\', 21.5, 76.9, 1200, 650)')
    if (useDBOn):
      if (not(apSensorOn) or ('ERROR' in airPressureString) ):
        DBairPressureString = "-999"
      else:
        DBairPressureString = airPressureString
         
      if (not(thSensorOn) or ('ERROR' in temperatureString) or ('ERROR' in humidityString)):
        DBtemperatureString = "-999"
        DBhumidityString = "-999"
      else:
        DBtemperatureString = temperatureString
        DBhumidityString = humidityString
      
      if (not(co2SensorOn) or ('ERROR' in co2String)):
        DBco2String = "-999"
      else:
        DBco2String = co2String
   
      logger.info("Inserting record into liv Measurements table:") 
      dbstring = "INSERT INTO Measurements VALUES (null, '" + str(timestamp) + "', " + \
        DBtemperatureString + ", " + DBhumidityString + ", " + DBairPressureString + ", " + DBco2String + ")" 
      logger.info(dbstring)
      try:
        c.execute(dbstring)
        dbconn.commit()  
      except:
        logger.error('Failed to insert record in the DB') 
 
    # LCD control code needs improvement
  
    for repeatDisplay in range(0, 3):
   
      for displayCounter in range(0, 4):
        if displayCounter == 0:
          line1 = "Air Pressure"
          line2 = airPressureString + " hPa"
        if displayCounter == 1:
          # if you live in North America, you probably use Fahrenheit
          # you can translate C to F if you want
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
               
