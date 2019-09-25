import json
import urllib2
import time

counter=0

while(1):
  counter += 1
   
  if (counter%2):
    print 'case 1'
    url1 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=2&nvalue=500'
    url2 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=1&nvalue=0&svalue=20;30;0;1000;0'
    page1 = urllib2.urlopen(url1).read()
    page2 = urllib2.urlopen(url2).read()
  else:
    print 'case 2'
    url1 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=2&nvalue=600'
    url2 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=1&nvalue=0&svalue=40;60;0;1100;0'
    page1 = urllib2.urlopen(url1).read()
    page2 = urllib2.urlopen(url2).read()
  time.sleep(60)
  
  '''
  url1 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=2&nvalue=11111'
  url2 = 'http://localhost:8080/json.htm?type=command&param=udevice&idx=1&nvalue=0&svalue=20;50;0;1001;0'
  page1 = urllib2.urlopen(url1).read()
  page2 = urllib2.urlopen(url2).read()
  time.sleep(60)
  '''