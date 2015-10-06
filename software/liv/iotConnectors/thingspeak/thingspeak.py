import httplib, urllib
import httplib2 as http
import datetime
import json
from urlparse import urlparse
import time


if __name__ == "__main__":
  apiKey = 'YOUR_API_KEY_HERE'
  ts_conn    = httplib.HTTPConnection("api.thingspeak.com:80")
  ts_headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

  target = urlparse('http://localhost:5000/getAllRawSensorData')
  method = 'GET'
  body = ''
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
  }

  h = http.Http()


while (1):
  print 'writing data to thingspeak '
  response, content = h.request(target.geturl(), method, body, headers)
  data = json.loads(content)
  print data
  now = datetime.datetime.utcnow()

  print now
  
  #ts_params = urllib.urlencode({'field1': '100', 'field2': '200', 'field3': '200', 'field4': '300', 'key': apiKey})
  ts_params = urllib.urlencode({'field1': data['CO2level'], 'field2': data['Temperature'], 'field3': data['Humidity'], 'field4': data['AirPressure'], 'key': apiKey})

  #headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  ts_conn.request("POST", "/update", ts_params, ts_headers)
  ts_response = ts_conn.getresponse()
  print ts_response.status, ts_response.reason
  data = ts_response.read()

  time.sleep(60)
    
