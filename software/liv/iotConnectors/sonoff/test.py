#!/usr/bin/env python

""" Simple http POST example using Python 2.7 and urllib and urllib2."""

import urllib
import urllib2
from urlparse import urlparse
import httplib2 as http
import json
import time

#url  = 'http//192.168.1.103/control?cmd=event,T1'

def main():

  print("hello test");

  url  = 'http//192.168.1.103/control?cmd=event,T1'
  target = urlparse(url)
  method = "POST"
  body = ''
  headers = {
                "Content-Type": "application/x-www-form-urlencoded", 
                "Accept": "text/plain"
  }
  
  h = http.Http()
  response, content = h.request(target.geturl, method, body, headers)
  print response
  print content

   

if __name__ == "__main__":
	main()





