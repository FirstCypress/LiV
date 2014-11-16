'''
Created by alfredc333
First Cypress Limited, 2014
MIT license
'''

import subprocess
import time
import re

class  temperatureHumiditySensor:

  def  __init__(self, sensorType, gpioNo):
    self.type = sensorType
    self.GPIO = gpioNo
    self.temperature = -9999
    self.humidity    = -9999
    

  def  readTemperatureHumidity(self):
    i = 1
    while (i < 11):
      try:
        subprocess.Popen(["./timer.sh"]);
        #logger.info('timer started in livDemo process')
        #logger.info('start Adafruit process')
        output = "EMPTY STRING"
        output = subprocess.check_output(["./Adafruit/Adafruit_DHT", self.type, self.GPIO]);
      except:
        # print "Unexpected error:", sys.exc_info()[0]
        #logger.info("Unexpected error! " + str(sys.exc_info()[0]))
        raise
        # print output
      matches = re.search("Temp =\s+([0-9.]+)", output)
      if (not matches):
        #logger.info('temp NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      temp = float(matches.group(1))
      #temperatureString = str(temp)

      # search for humidity printout
      matches = re.search("Hum =\s+([0-9.]+)", output)
      if (not matches):
        #logger.info('humidity NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      hum = float(matches.group(1))
      #humidityString = str(humidity)
      self.temperature = temp
      self.humidity = hum
      break

  def readTemperature(self):
    return self.temperature
  
  def readHumidity(self):
    return self.humidity
  



if __name__ == "__main__":

  print 'testing DHT temp and humidity Sensor'
  thSensor = temperatureHumiditySensor('22', '17')
  thSensor.readTemperatureHumidity()
  t = thSensor.readTemperature()
  h = thSensor.readHumidity()

  print 'temperature is ' + str(t)
  print 'humidity is ' + str(h)
