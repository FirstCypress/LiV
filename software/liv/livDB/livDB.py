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
from co2Sensor import co2Sensor 
from airPressureSensor import airPressureSensor
from temperatureHumiditySensor import temperatureHumiditySensor

# Read parameters from configuration file
config = ConfigParser.ConfigParser()
config.read('./livDB.config')

thSensorOn = config.getboolean('ON_BOARD_SENSORS', 'temp_humidity_sensor')
apSensorOn = config.getboolean('ON_BOARD_SENSORS', 'air_pressure_sensor')
co2SensorOn = config.getboolean('ON_BOARD_SENSORS', 'co2_sensor')

apAddress = config.get('AIR_PRESSURE_SENSOR', 'I2C_address')

thType = config.get('TEMP_HUMIDITY_SENSOR', 'type')
thGPIO = config.get('TEMP_HUMIDITY_SENSOR', 'gpio_no')

sensorReadTime = config.getfloat('READ_CYCLE','read_time')

#read format C/F, hPa/inchHg
tempFormat = config.get('FORMAT','temperature') 
airpressureFormat = config.get('FORMAT','airpressure')

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

logger.info('--------------------------------------------')
logger.info('LIV STARTED')

temperatureString = 'NO TEMP SENSOR';
humidityString = 'NO HUM SENSOR';
airPressureString = 'NO AP SENSOR';
co2String = 'NO CO2 SENSOR';


# Initialize airPressure sensor if present
# BMP085 and use HIGH RESOLUTION mode
if (apSensorOn):
  try:
    #airPressureString = "ERROR";
    bmp = airPressureSensor(3, int(apAddress, 16))
    logger.info('Air pressure sensor initialized')
  except:
    logger.critical('Air pressure sensor failed to initialize')
    sys.exit(1)
    
# initialize CO2 sensor if present
# to do list: add raise error code in constructor
if (co2SensorOn):
  try:
    #co2String = 'ERROR'
    co2s = co2Sensor()
    logger.info('co2 sensor initialized')
  except:
    logger.critical('co2 sensor failed to initialize')
    sys.exit(1)
# initialize temp and humidity sensor if present
if (thSensorOn):
  try:
    temperatureString = 'ERROR';
    humidityString = 'ERROR';
    ts = temperatureHumiditySensor(thType, thGPIO, logger)
    logger.info('Temp and Humidity sensor initialized')
  except:
    logger.critical('Temp and Humidity sensor failed to initialize')
    sys.exit(1)
    
    
# initialize db connection 
# conect to sqlite DB
  try:
    dbconn = sqlite3.connect('liv.db')
    c = dbconn.cursor()
    logger.info('sqlite DB Connection initialized')
  except:
    logger.critical('sqlite DB Failed to initialize')
    sys.exit(1)
    
    
  while(True):
    if(thSensorOn):
      try:  
        temperatureString, humidityString = ts.readTemperatureHumidity()
        #fix for sensor reading errors
        #test line humidityString ='3001'
        h = float(humidityString)
        while(h > 100):
            time.sleep(20)
            logger.error('humidity reading error ' + humidityString)
            temperatureString, humidityString = ts.readTemperatureHumidity()
            h = float(humidityString) 
        
        #convert to F if needed
        if tempFormat == 'F':
          temperatureString = str (9.0/5.0*float(temperatureString) + 32)  
      except:
        temperatureString = 'ERROR'
        humidityString = 'ERROR'    

    if(apSensorOn):
      try:
        pressure = bmp.readAirPressure()
        #convert to inchHg if needed
        if airpressureFormat == 'inchHg':
          pressure = str (0.0295300*pressure)
        airPressureString = str(pressure)
      except:
        airPressureString = 'ERROR'
        logger.error('Failed to read air pressure sensor')

    if(co2SensorOn):
      try:
        co2 = co2s.readCO2Level()
        co2String = str(co2)
      except:
        co2String = 'ERROR'
        logger.error('Failed to read co2 sensor')

   
    logger.info("AirPressure:  " + airPressureString) 
    logger.info("Temperature:  " + temperatureString)
    logger.info("Humidity:     " + humidityString)
    logger.info("CO2 = " + co2String)
 
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
 
    # WRITE RECORD IN THE DB HERE
    # 'INSERT INTO Measurements VALUES(null ,\'2014-01-28 10:37:09\', 21.5, 76.9, 1200, 650)')
    if (not(apSensorOn) or ('ERROR' in airPressureString)):
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
      logger.error("Failed to insert record in liv DB")
    time.sleep(sensorReadTime)
 
