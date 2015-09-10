'''
Created on August 27, 2014 by alfredc333

'''

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
from lcd16x2 import lcd16x2

# Read parameters from configuration file
config = ConfigParser.ConfigParser()
config.read('./livLCD.config')

LCDAddress = config.get('LCD_DISPLAY', 'I2C_address')
LCDPort = config.getint('LCD_DISPLAY', 'port_no')

displayTime = config.getfloat('LCD_CYCLE_TIME', 'display_time')
displayCycles = config.getint('LCD_CYCLE_TIME', 'no_of_cycles')


logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

logger.info('--------------------------------------------')
logger.info('LIV LCD STARTED')


# LCD init code 
try:
  lcd = lcd16x2(int(LCDAddress, 16), LCDPort)
  lcd.initDisplay()
  logger.info('LCD initialized')
except:
  logger.critical('Failed to initialize LCD')
  sys.exit(1)

# read last readings directly from database, so I can have LCD working 
# even when livAPIs is down so:
# initialize db connection 
# conect to sqlite DB
try:
  dbconn = sqlite3.connect('../livDB/liv.db')
  dbconn.row_factory = sqlite3.Row
  logger.info('sqlite DB connection initialized')
except:
  logger.critical('sqlite DB Failed to initialize')
  sys.exit(1)
  
#some variables here
sensorNames = ['temperature', 'humidity', 'airpressure', 'co2']  
displayStrings = {'temperature': "Temperature", 'humidity': "Humidity", 'airpressure': "Air Pressure", 'co2': "CO2 Level"}
onBoardSensors = {'temperature' :False, 'humidity': False, 'airpressure': False, 'co2': False}
config.read('../livDB/livDB.config')
onBoardSensors['temperature'] = config.getboolean('ON_BOARD_SENSORS', 'temp_humidity_sensor')
onBoardSensors['humidity'] = config.getboolean('ON_BOARD_SENSORS', 'temp_humidity_sensor')
onBoardSensors['airpressure'] = config.getboolean('ON_BOARD_SENSORS', 'air_pressure_sensor')
onBoardSensors['co2'] = config.getboolean('ON_BOARD_SENSORS', 'co2_sensor')
logger.info('onBoardSensors:')
logger.info(onBoardSensors)
  
lcd.cleanFirstLine()
lcd.cleanSecondLine()
    
while(True):
  config.read('./livLCD.config')
  #read alarm levels from config file, currently blink measurement only if
  #measured value is higher then threshold
  CO2_ALARM = config.getfloat('ALARM_LEVELS', 'co2')
  T_ALARM = config.getfloat('ALARM_LEVELS', 'temperature')
  H_ALARM = config.getfloat('ALARM_LEVELS', 'humidity')
  AP_ALARM = config.getfloat('ALARM_LEVELS', 'airPressure')
  alarmLevels = {'temperature':T_ALARM, 'humidity':H_ALARM, 'airpressure':AP_ALARM, 'co2':CO2_ALARM}
  alarmValues={'temperature': False, 'humidity':False, 'airpressure':False, 'co2':False}
  
  
  #read last measurement directly from database, don't use local APIs so LCD display works even if 
  #LiV APIs process is down 
  dbData={}
  dbDisplayData={}
  
  try:
    logger.info("start retrieve last sqlite record")
    query = 'SELECT * from Measurements ORDER By Mid DESC LIMIT 1'
    cursor = dbconn.execute(query)
    
    for row in cursor:
      #print row
      t = str(row["Temperature"])
      h = str(row["Humidity"])
      ap = str(row["AirPressure"])
      timeStamp = row["Timestamp"]
      co2 = str(row["CO2level"])
      dbData ={'temperature':t, 'humidity':h, 'airpressure':ap, 'co2':co2}

      logger.info("Succesfully retrieved db Data: ")
      logger.info("Time Stamp = " + timeStamp)
      logger.info("alarmLevels are: ")
      logger.info(alarmLevels)
      logger.info("dbData is: ")
      logger.info(dbData)
      
      for m, s in enumerate(sensorNames):
        if (float(dbData[s]) > float(alarmLevels[s])):
          alarmValues[s] = True
      
      #dbDisplayData = [dbData[0]+' C', dbData[1]+' %',dbData[2]+' ppm',dbData[3]+' hPa']
      dbDisplayData = {'temperature': dbData['temperature']+' C','humidity': dbData['humidity']+' %', 'airpressure':dbData['airpressure']+ ' hPa', 'co2': dbData['co2']+' ppm'}
      
  
  except:
    dbDisplayData ={'temperature':"error", 'humidity':"error", 'airpressure':"error", 'co2':"error"}
    alarmValues = {'temperature':True, 'humidity':True, 'airpressure':True, 'co2':True}
    logger.critical("Failed to retrieve record")
    sys.exit(1)
  
  #display only measurements for onBoard Sensors

  dStrings = dict(displayStrings)
  dData = dict(dbDisplayData)
  aValues = dict(alarmValues)

  for i, v in enumerate(sensorNames):
    if onBoardSensors[v] == False:
      del dStrings[v]
      del dData[v]
      del aValues[v]

  lcdDisplayData = zip(dStrings.values(),dData.values()) 
  
  
  for x in range(0,displayCycles):
    i=0
    for idx, l in enumerate(lcdDisplayData):
      # First line first column
      lcd.cleanFirstLine()        
      # Second line first column
      lcd.cleanSecondLine()    
      
      lcd.writeFirstLine(l[0])
      if (aValues.values()[idx] == True):
        #blink every 0.5 seconds
        t=0
        while(t < displayTime):
          lcd.writeSecondLine(l[1])
          time.sleep(0.5)
          lcd.cleanSecondLine()
          time.sleep(0.5)
          t=t+1
      else:
        lcd.writeSecondLine(l[1])
        time.sleep(displayTime)
#         time.sleep(2)
      i=i+1
