import httplib
import httplib2 as http
import datetime
import json
from urlparse import urlparse
import requests
import time
import sys
import logging
import logging.config
import ConfigParser

if __name__ == "__main__":
 
  logging.config.fileConfig('logging.ini')
  logger = logging.getLogger(__name__)

  logger.info('--------------------------------------------')
  logger.info('IFTTT STARTED')   
  
  try:
    config = ConfigParser.ConfigParser()
    config.read('./ifttt.config')
    reportTime = config.getint('IFTTT', 'loop_time')
    iftttKey = config.get('IFTTT', 'ifttt_maker_key')
    iftttBaseUrl = config.get('IFTTT', 'ifttt_base_url')
    
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
    

while (1):
  logger.info('enter IFTTT loop ')
  try:
    #retrieve latest measurements
    response, content = h.request(target.geturl(), method, body, headers)
    data = json.loads(content)
    
    logger.info('retrieved Measurements:   ' + content)
    
    
    #trigger IFTTT events  
    url_twitter = iftttBaseUrl + 'liv_twitter_event' +'/with/key/'+iftttKey
    url_email = iftttBaseUrl + 'liv_email_event' +'/with/key/'+iftttKey
    
    d= {'value1': data['CO2level'], 'value2': data['Temperature'], 'value3': data['Humidity'], 'value4': data['AirPressure']}
    
    #trigger liv_twitter_event IFTTT Recipe ID 41012795
    r = requests.post(url_twitter,d)
    logger.info('IFTT liv_twitter_event response: ' + str(r.status_code))
    
    #trigger liv_email_event IFTTT Recipe ID 41051386
    r = requests.post(url_email,d)
    logger.info('IFTT liv_email_event response: ' + str(r.status_code))
    
  except:
    e = sys.exc_info()[0]
    logger.critical(e)
    #print "exception"

  time.sleep(reportTime)
    
