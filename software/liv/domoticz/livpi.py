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
import urllib2

if __name__ == "__main__":
 
  logging.config.fileConfig('logging.ini')
  logger = logging.getLogger(__name__)

  logger.info('--------------------------------------------')
  logger.info('LIVPI DOMOTICZ PROCESS STARTED')   
  logger.info('Pushing LiV Pi measurements into Domoticz')
  
  try:
    
    config = ConfigParser.ConfigParser()
    config.read('./livpi.config')
    reportTime = config.getint('DOMOTICZ', 'report_time')

    #prepare for local liv APIs connection     
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
  logger.info('Writing data to LiV Pi Sensors in Domoticz ')
  try:
    domoticz_conn    = httplib.HTTPConnection("localhost:8080")
    
    response, content = h.request(target.geturl(), method, body, headers)
    data = json.loads(content)
    logger.info(data)
    
    url_CO2 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=2&nvalue=' +str(data['CO2level'])
    pageCO2 = urllib2.urlopen(url_CO2).read()
    logger.info('wrote CO2 level to Domoticz')
    
    url_THB = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=1&nvalue=0&svalue=' + \
       str(data['Temperature']) + ';'+ str(data['Humidity']) + ';0;'+ str(data['AirPressure']) +';0'
    
    #print url_THB
    
    pageTHB = urllib2.urlopen(url_THB).read()
    logger.info('wrote THB levels to Domoticz')
    
    now = datetime.datetime.utcnow()
    logger.info(now)
        

  except:
    e = sys.exc_info()[0]
    logger.critical(e)
    #print "exception"

  time.sleep(reportTime)
    
