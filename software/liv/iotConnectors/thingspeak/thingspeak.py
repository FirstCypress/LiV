import httplib, urllib
import httplib2 as http
import datetime
import json
from urlparse import urlparse
import time
import sys
import logging
import logging.config
import ConfigParser

if __name__ == "__main__":
 
  logging.config.fileConfig('logging.ini')
  logger = logging.getLogger(__name__)

  logger.info('--------------------------------------------')
  logger.info('THINGSPEAK STARTED')   

  try:
    config = ConfigParser.ConfigParser()
    config.read('./thingspeak.config')
    apiKey = config.get('THINGSPEAK', 'write_api_key')
    reportTime = config.getint('THINGSPEAK', 'report_time')
   
    ts_headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

    target = urlparse('http://localhost:5000/getAllRawSensorData')
    method = 'GET'
    body = ''
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
    }

    h = http.Http()
  except:
    e = sys.exc_info()[0]
    logger.critical(e)
    #print e
    

while (1):
  logger.info('Writing data to thingspeak ')
  try:
    ts_conn    = httplib.HTTPConnection("api.thingspeak.com:80")
    response, content = h.request(target.geturl(), method, body, headers)
    data = json.loads(content)
    
    logger.info(data)
    now = datetime.datetime.utcnow()
    logger.info(now)

    #print now
  
    #ts_params = urllib.urlencode({'field1': '100', 'field2': '200', 'field3': '200', 'field4': '300', 'key': apiKey})
    ts_params = urllib.urlencode({'field1': data['CO2level'], 'field2': data['Temperature'], 'field3': data['Humidity'], 'field4': data['AirPressure'], 'key': apiKey})

    ts_conn.request("POST", "/update", ts_params, ts_headers)

    ts_response = ts_conn.getresponse()
    #print ts_response.status, ts_response.reason
    logger.info(ts_response.status)
    logger.info(ts_response.reason)
    #d = ts_respond.read()

  except:
    e = sys.exc_info()[0]
    logger.critical(e)
    #print "exception"

  time.sleep(reportTime)
    
