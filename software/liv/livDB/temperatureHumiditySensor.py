import subprocess
import time
import re
import sys
import logging
import logging.config

class  temperatureHumiditySensor:

  def  __init__(self, sensorType, gpioNo, log):
    self.type = sensorType
    self.GPIO = gpioNo
    self.logger      = log
    self.temperature = 'ERROR'
    self.humidity    = 'ERROR'

    

  def  readTemperatureHumidity(self):
    i = 1
    while (i < 6):
      try:
        subprocess.Popen(["./timer.sh"]);
        output = "EMPTY STRING"
        #OLD DRIVER output = subprocess.check_output(["./Adafruit/Adafruit_DHT", self.type, self.GPIO]);
        output = subprocess.check_output(["./Adafruit_Python_DHT/examples/AdafruitDHT.py", self.type, self.GPIO]);
      except:
        self.logger.error("Unexpected error! " + str(sys.exc_info()[0]))
        self.logger.error("Make sure temp sensor is connected ")

      #search for temperature printout
      #OLD DRIVER matches = re.search("Temp =\s+([0-9.]+)", output)
      matches = re.search("Temp=+([0-9.]+)", output)
      if (not matches):
        self.logger.error('temp NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      temp = matches.group(1)

      # search for humidity printout
      #OLD DRIVER matches = re.search("Hum =\s+([0-9.]+)", output)
      matches = re.search("Humidity=+([0-9.]+)", output)
      if (not matches):
        self.logger.error('humidity NOT MATCH ' + output)
        time.sleep(5)
        i += 1
        continue
      hum = matches.group(1)
      
      return temp, hum
    
    return self.temperature, self.humidity
  
  


if __name__ == "__main__":

  print 'testing DHT temp and humidity Sensor'
  logging.config.fileConfig('logging.ini')
  log = logging.getLogger(__name__)
  
  thSensor = temperatureHumiditySensor('22', '17', log)
  t, h = thSensor.readTemperatureHumidity()
  
  thSensor.logger.info('Test temperature sensor: ' + t )
  thSensor.logger.info('Test humidity sensor: ' + h )
  
  print 'temperature is ' + str(t)
  print 'humidity is ' + str(h)
