import httplib, urllib
import httplib2 as http
import datetime
import json
from urlparse import urlparse
import time


if __name__ == "__main__":
  apiKey = 'YOUR_API_KEY_HERE'
  e_conn    = httplib.HTTPConnection("emoncms.org:80")
  e_headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

  target = urlparse('http://localhost:5000/getAllRawSensorData')
  method = 'GET'
  body = ''
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
  }

  h = http.Http()


while (1):
  print 'writing data to emoncms'
  response, content = h.request(target.geturl(), method, body, headers)
  data = json.loads(content)
  print data
  now = datetime.datetime.utcnow()

  print now
  
  #ts_params = urllib.urlencode({'field1': '100', 'field2': '200', 'field3': '200', 'field4': '300', 'key': apiKey})
  #e_params = urllib.urlencode({'field1': data['CO2level'], 'field2': data['Temperature'], 'field3': data['Humidity'], 'field4': data['AirPressure'], 'key': apiKey})
  
  
  url = "http://emoncms.org/input/post.json? \
     json={co2:" +data['CO2level'] +",temperature:" +data['Temperature']+",humidity:" +data['Humidity'] +",airPressure:" +data['AirPressure'] +"}" \
     +"&apikey=4e206bf15f81dcedf72a5ae10f06ae1c"
  
  print url
  urllib.urlopen(url)

  #headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  #e_conn.request("POST", "/api", e_params, e_headers)
  #e_response = e_conn.getresponse()
  #print e_response.status, e_response.reason
  #data = e_response.read()

  time.sleep(60)
    
  
