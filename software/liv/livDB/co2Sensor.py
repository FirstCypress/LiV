import serial
import time


class  co2Sensor:

  def  __init__(self):
    self.ser = serial.Serial("/dev/ttyAMA0")
    self.ser.flushInput()


  def readCO2Level(self):
    # read K30 CO2 from serial 
    self.ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.01)
    resp = self.ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    co2 = (high * 256) + low
    return co2
  


if __name__ == "__main__":

  print 'testing CO2 Sensor'

  co2Sensor = co2Sensor()
  co2 = co2Sensor.readCO2Level()


  print 'co2 level is ' + str(co2)

