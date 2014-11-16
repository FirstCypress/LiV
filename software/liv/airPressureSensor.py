'''
Created by alfredc333
First Cypress Limited, 2014
MIT license
'''

from Adafruit.Adafruit_BMP085 import BMP085


class  airPressureSensor:

  def  __init__(self, addr):
    self.bmp = BMP085(addr)



  def  readAirPressure(self):
    pressure = self.bmp.readPressure()
    airPressure = pressure / 100.0
    return airPressure



  def  readTemperature(self):
    temperature = self.bmp.readTemperature()
    return temperature



  def  readAltitude(self):
    altitude = self.bmp.readAltitude()
    return altitude


#use default address 0x77, port 1 is default in Adafruit
if __name__ == "__main__":

  print 'testing BMP085 / BMP180 air pressure Sensor'

  apSensor = airPressureSensor(0x77)
  t = apSensor.readTemperature()
  a = apSensor.readAltitude()
  ap = apSensor.readAirPressure()

  print 'air pressure is ' + str(ap)
  print 'temperature is  ' + str(t)
  print 'altitude is     ' + str(a)


    #except:
