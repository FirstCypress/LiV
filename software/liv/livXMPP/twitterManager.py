import sys
import ConfigParser
import logging
import logging.config
from twitter import * 


class  twitterManager:

  def  __init__(self, log ):
    self.logger = log
    config = ConfigParser.ConfigParser()
    config.read("./twitter.config")
  
    self.livDeviceName    = config.get('TWITTER', 'liv_device_name')
    self.alarmActive   = config.getboolean('TWITTER', 'twitter_alarm_active')
    self.reportActive  = config.getboolean('TWITTER', 'twitter_report_active')
    self.reportTime    = config.getint('TWITTER', 'twitter_report_time')
    
    self.token         = config.get('TWITTER', 'token')
    self.tokenKey      = config.get('TWITTER', 'token_key')
    self.conSecret     = config.get('TWITTER', 'con_secret')
    self.conSecretKey  = config.get('TWITTER', 'con_secret_key')
    
    self.minuteCounter = 0
  
  
  def sendTweet(self, type, message):
    try:      
      print("get twitter class")
      #m1 = message + "  " + "#RaspberryPi "  +"#livpi"
      #t = Twitter(auth=OAuth("28595681-sk4FFlQxfJKmIWyb8L7X30t3ttHHSDazN5wWqLIWx", "nXn4qyIJwWZsmvd5Mfyufnz1UQuyXxTHRLgbrpLVeu885", "iFxQg6wgCBXzlq1lWZwB164l1", "w3wOy2uUSGHA2yTAC6TqjJ8xlIUVKcicOf2GuhBIEJnb6UjdjM"))  
      t = Twitter(auth=OAuth(self.token, self.tokenKey, self.conSecret, self.conSecretKey))
      s = self.livDeviceName +'  '+ type + '   ' + message
      t.statuses.update(status=s)
      self.logger.info("LiV sent a tweet  " + s)  
    except:
      e = sys.exc_info()[0]
      self.logger.critical(e)
      
  
  def getTwitterAlarmFlag(self):
    return self.alarmActive
  
  def sendTwitterReportNow(self):
    if self.minuteCounter == self.reportTime:  
      return True
    else:
      return False      
          
  def getTwitterReportFlag(self):
    return self.reportActive  
      
  
  def incrementMinuteCounter(self):
      self.minuteCounter +=1
  
  
  def resetMinuteCounter(self):
      self.minuteCounter = 0  

    
if __name__ == "__main__":
  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  
  tm = twitterManager(logger)
  print "twitterAlarmFlag" + "   " + str(tm.alarmActive)
  print "twitterReportFlag" + "   " + str(tm.reportActive)
  print "token  " + "   " + str(tm.token)
  print "token key " + "   " + str(tm.tokenKey)
  print "con secret  " + "   " + str(tm.conSecret)
  print "con secret key  " + "   " + str(tm.conSecretKey)
  
  if tm.alarmActive == True:
    tm.sendTweet("Alarm", "this is an alarm test")
    print "sent alarm tweet"  
    #tm.sendTweet("LiV Alarm Notification", "here is the alarm")
    
  
  if tm.reportActive == True:
    #tm.sendTweet("Report", "report test")  
    print "send report tweet"    
    #em.sendTweet("LiV Report", "here is the report")
  
  
  
  
  