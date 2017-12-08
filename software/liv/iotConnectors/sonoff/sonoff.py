#!/usr/bin/env python

""" sonoff control from LiV Pi"""

import sys
import ConfigParser
import urllib
import urllib2
from urlparse import urlparse
import httplib2 as http
import json
import time
import logging
import logging.config
import requests

def main():

  logging.config.fileConfig('logging.ini')
  logger = logging.getLogger(__name__)

  logger.info('--------------------------------------------')
  logger.info('SONOFF CONTROL STARTED')
  
  config = ConfigParser.ConfigParser()
  config.read("./sonoff.config")
 
  device_control  = config.getboolean('SONOFF', 'sonoff_control')
  if (device_control == True):
      action = config.get('SONOFF','action')
      level  = config.getint('SONOFF','level')
      switch_on_higher = config.getboolean('SONOFF','sonoff_switch_on_higher')
      sonoff_IP = config.get('SONOFF', 'sonoff_IP')
      rule_on = config.get('SONOFF', 'sonoff_rule_on')
      rule_off = config.get('SONOFF', 'sonoff_rule_off')
      loop_time = config.getint('SONOFF', 'sonoff_loop_time')
  else:
      logger.info('EXIT SONOFF CONTROL: CONTROL FLAG set to False')
      sys.exit()
 	
  sonoff_turn_on  = "http://" + sonoff_IP + "/control?" + rule_on
  sonoff_turn_off = "http://" + sonoff_IP + "/control?" + rule_off

  print(sonoff_turn_on)
  print(sonoff_turn_off)
  
  target = urlparse('http://localhost:5000/getAllRawSensorData')
  method = 'GET'
  body = ''
  headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

  h = http.Http()  
  
  while(True):
    logger.info('enter one more loop')  
    response, content = h.request(target.geturl(), method, body, headers)
    print response
    print content
    m = json.loads(content)
    '''print m["AirPressure"]
    print m["Humidity"]
    print m["AirPressure"]
    print m["CO2level"]'''

    temp = m["Temperature"]
    hum  = m["Humidity"]
    ap   = m["AirPressure"]
    co2  = m["CO2level"]
    
    if action == "CO2":
    	l = int(m["CO2level"])
    elif action == "Temp":
    	l = float(m["Temperature"])
    elif action == "Hum":
    	l = float(m["Humidity"])
    elif action == "Ap":
    	l = float(m["AirPressure"])
    else:
    	logger.critical("UNKNOWN ACTION TYPE")
    	sys.exit()
    	
    
    sonoff_url ="uninitialized"
    print("Measured level is:   " + str(l))
    print("Threshold is     :   " + str(level))
    
    if switch_on_higher == True:
      if l > level:
        print("turn on because higher")
        sonoff_url = sonoff_turn_on
      else:
        print("turn off because lower")
        sonoff_url = sonoff_turn_off
    else:
      if l < level:
        print("turn on because lower")
        sonoff_url = sonoff_turn_on
      else:
        print("turn off because higher")
        sonoff_url = sonoff_turn_off   
    
    try:
      r = requests.post(sonoff_url)
      if r.status_code == 200:
          logger.info("Sonoff return code: SUCCESS")
      else:
          logger.info("Sonoff return code: FAILED")
    except Exception:
      logger.critical("UNABLE TO SEND COMMAND TO SONOFF")  
      logging.exception("error code: ")		
    
    time.sleep(loop_time)
  

if __name__ == "__main__":
	main()


