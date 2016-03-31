import xively
import datetime
import httplib2 as http
import json
from urlparse import urlparse
import time

api = xively.XivelyAPIClient("YOUR_API_KEY")
feed = api.feeds.get(YOUR_FEED)



target = urlparse('http://localhost:5000/getAllRawSensorData')
method = 'GET'
body = ''
headers = {
'Accept': 'application/json',
'Content-Type': 'application/json; charset=UTF-8'
}

h = http.Http()
response, content = h.request(target.geturl(), method, body, headers)
data = json.loads(content)


while (1):
  print 'writing data to xively '
  response, content = h.request(target.geturl(), method, body, headers)
  data = json.loads(content)
  print data
  now = datetime.datetime.utcnow()
  #now = datetime.datetime.now()
  print now
  feed.datastreams = [
    xively.Datastream(id='airpressure', current_value=data['AirPressure'], at=now),
    xively.Datastream(id='co2', current_value=data['CO2level'], at=now),
    xively.Datastream(id='humidity', current_value=data['Humidity'], at=now),
    xively.Datastream(id='temperature', current_value=data['Temperature'], at=now),
]

  feed.update()
  #break
  time.sleep(120)
