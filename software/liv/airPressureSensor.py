
from Adafruit_Python_BMP.Adafruit_BMP import BMP085
#OLD VERSION from Adafruit.Adafruit_BMP085 import BMP085


class  airPressureSensor:

  def  __init__(self, mode, addr):
    #set high resolution mode and I2C address
    self.bmp = BMP085.BMP085(mode, addr)


  def  readAirPressure(self):
    pressure = self.bmp.read_pressure()
    airPressure = pressure / 100.0
    return airPressure


  def  readTemperature(self):
    temperature = self.bmp.read_temperature()
    return temperature


  def  readAltitude(self):
    altitude = self.bmp.read_altitude()
    return altitude


#use default address 0x77, port 1 is default in Adafruit
if __name__ == "__main__":

  print 'testing BMP085 / BMP180 air pressure Sensor'

  apSensor = airPressureSensor(3, 0x77)
  t = apSensor.readTemperature()
  a = apSensor.readAltitude()
  ap = apSensor.readAirPressure()

  print 'air pressure is ' + str(ap)
  print 'temperature is  ' + str(t)
  print 'altitude is     ' + str(a)


    #except:
