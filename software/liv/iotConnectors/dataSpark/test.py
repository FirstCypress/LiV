#!/usr/bin/env python

""" Simple http POST example using Python 2.7 and urllib and urllib2."""

import urllib
import urllib2
from urlparse import urlparse
import httplib2 as http
import json
import time

public_hash     = 'YOUR_PUBLIC_HASH'
private_hash    = 'YOUR_PRIVATE_HASH'
base_url        = 'https://data.sparkfun.com'
post_url        = base_url + '/input/' + public_hash


headers = {
	'Content-type': 'application/x-www-form-urlencoded',
	'Phant-Private-Key': private_hash
}


def main():


 while(True):
  target = urlparse('http://localhost:5000/getAllRawSensorData')
  method = 'GET'
  body = ''
  headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json; charset=UTF-8'
  }

  h = http.Http()
  response, content = h.request(target.geturl(), method, body, headers)
  print response
  print content
  m = json.loads(content)
  print m["AirPressure"]
  print m["Humidity"]
  print m["AirPressure"]
  print m["CO2level"]


  data = {}
  data['temperature'] = m["Temperature"]
  data['humidity'] = m["Humidity"]
  data['airpressure'] = m["AirPressure"]
  data['co2level'] = m["CO2level"]
  headers = {
	 'Content-type': 'application/x-www-form-urlencoded',
	 'Phant-Private-Key': private_hash
  }
  data = urllib.urlencode(data)
  post_request = urllib2.Request(post_url,data,headers)

  try: 
    post_response = urllib2.urlopen(post_request)
    print post_response.read()

  except URLError as e:
    print "Error: ", e.reason
  
  time.sleep(300)

if __name__ == "__main__":
	main()









