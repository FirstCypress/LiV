import smbus  
import time  

class  lcd16x2:  

  def  __init__(self, addr, port):
    self.bus = smbus.SMBus (port)
    self.addr = addr
    self.cleanLine = '                '   

  def  writeCommand (self, command):
    self.bus.write_byte (self.addr, 0b1100 | command << 4)
    time.sleep (0.005)
    self.bus.write_byte (self.addr, 0b1000 | command << 4)
    time.sleep (0.005)

  def  writeWord (self, word):
    for i in range (0, len (word)):
      asciiCode = ord (word [i])
      self.bus.write_byte (self.addr, 0b1101 | (asciiCode >> 4 & 0x0F) << 4)
      time.sleep (0.0005)
      self.bus.write_byte (self.addr, 0b1001 | (asciiCode >> 4 & 0x0F) << 4)
      time.sleep (0.0005)
      self.bus.write_byte (self.addr, 0b1101 | (asciiCode & 0x0F) << 4)
      time.sleep (0.0005)
      self.bus.write_byte (self.addr, 0b1001 | (asciiCode & 0x0F) << 4)
      time.sleep (0.0005)

  def initDisplay(self):
    # Init 1602 LCD display
    self.writeCommand (0b0010)
    # 4-byte mode, 2 line code
    self.writeCommand (0b0010)
    self.writeCommand (0b1111)
    # Set cursor mode
    self.writeCommand (0b0000)
    self.writeCommand (0b1100)
    # Cursor shift mode
    self.writeCommand (0b0000)
    self.writeCommand (0b0110)

  def writeFirstLine(self, word):
    # First line first column
    self.writeCommand (0b1000)
    self.writeCommand (0b0000)
    self.writeWord (word)

  def writeSecondLine(self, word):  
    #Second line first column
    self.writeCommand (0b1100)
    self.writeCommand (0b0000)
    self.writeWord (word)

  def cleanFirstLine(self):
    # First line first column
    self.writeCommand (0b1000)
    self.writeCommand (0b0000)
    self.writeWord (self.cleanLine)

  def cleanSecondLine(self):  
    #Second line first column
    self.writeCommand (0b1100)
    self.writeCommand (0b0000)
    self.writeWord (self.cleanLine)

#use default address 0x27, port 1 for main
if __name__ == "__main__":

  lcd = lcd16x2(0x27, 1)
  lcd.initDisplay()
  while(True):
    lcd.writeFirstLine('Test First Line')
    lcd.writeSecondLine('Test Second Line')
    time.sleep(5)
    lcd.cleanFirstLine()
    lcd.cleanSecondLine()
    print 'testing LCD display. please check display'
      
