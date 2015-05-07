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

displayStrings = ["Temperature", "Humidity", "CO2 Level", "Air Pressure"]


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
  logger.error('Failed to initialize LCD')
  
# read last readings directly from database, don't use local APIs
# initialize db connection 
# conect to sqlite DB
try:
  dbconn = sqlite3.connect('../livDB/liv.db')
  dbconn.row_factory = sqlite3.Row

  logger.info('sqlite DB connection initialized')
except:
  logger.error('sqlite DB Failed to initialize')
  
lcd.cleanFirstLine()
lcd.cleanSecondLine()
    
while(True):
  config.read('./livLCD.config')
  #set alarm level
  CO2_ALARM = config.getfloat('ALARM_LEVELS', 'co2')
  TEMP_ALARM = config.getfloat('ALARM_LEVELS', 'temperature')
  HUMID_ALARM = config.getfloat('ALARM_LEVELS', 'humidity')
  AP_ALARM = config.getfloat('ALARM_LEVELS', 'airPressure')
  alarmLevels = [TEMP_ALARM, HUMID_ALARM, CO2_ALARM, AP_ALARM]
    # read last readings directly from database, don't use local APIs  
  dbData=[]
  dbDisplayData=[]
  alarmValues=[False, False, False, False]
  
  try:
    logger.info("start retrieve last sqlite record")
    query = 'SELECT * from Measurements ORDER By Mid DESC LIMIT 1'
    
    cursor = dbconn.execute(query)
    
    for row in cursor:
      #print row
      temperature = str(row["Temperature"])
      humidity = str(row["Humidity"])
      airPressure = str(row["AirPressure"])
      timeStamp = row["Timestamp"]
      co2 = str(row["CO2level"])
      dbData =[temperature, humidity, co2, airPressure]
      logger.info("Succesfully retrieved db Data: ")
      logger.info("Temperature = " + temperature)
      logger.info("Humidity = " + humidity)
      logger.info("Air Pressure = " + airPressure)
      logger.info("CO2 Level = " + co2)
      logger.info("Time Stamp = " + timeStamp)
      logger.info("alarmLevels are: ")
      logger.info(alarmLevels)
      logger.info("dbData is: ")
      logger.info(dbData)
      
      for index, d in enumerate(dbData):
        if (float(d) > alarmLevels[index]):
           alarmValues[index] = True
      dbDisplayData = [dbData[0]+' C', dbData[1]+' %',dbData[2]+' ppm',dbData[3]+' hPa']
  except:
    temperature ="error"
    humidity ="error"
    airPressure="error"
    co2="error"
    dbDisplayData =[temperature, humidity, co2, airPressure]
    alarmValues = [True, True, True, True]
    logger.error("Failed to retrieve record")
  
  lcdDisplayData = zip(displayStrings,dbDisplayData) 
  
  

  for x in range(0,displayCycles):
    i=0
    for idx, l in enumerate(lcdDisplayData):
      # First line first column
      lcd.cleanFirstLine()        
      # Second line first column
      lcd.cleanSecondLine()    
      
      lcd.writeFirstLine(l[0])
      if (alarmValues[idx] == True):
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
