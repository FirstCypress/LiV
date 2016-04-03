import sys
import ConfigParser
import logging
import logging.config
import tweepy
from tweepy.auth import OAuthHandler
from tweepy.streaming import StreamListener, Stream

class  twitterManager:

  def  __init__(self, log ):
    self.logger = log
    config = ConfigParser.ConfigParser()
    config.read("./twitter.config")
  
    self.livDeviceName = config.get('TWITTER', 'liv_device_name')
    self.alarmActive   = config.getboolean('TWITTER', 'twitter_alarm_active')
    self.reportActive  = config.getboolean('TWITTER', 'twitter_report_active')
    self.reportTime    = config.getint('TWITTER', 'twitter_report_time')
    
    self.accessToken         = config.get('TWITTER', 'access_token')
    self.accessTokenSecret      = config.get('TWITTER', 'access_token_secret')
    self.consumerKey  = config.get('TWITTER', 'consumer_key')
    self.consumerSecret     = config.get('TWITTER', 'consumer_secret')
    
    self.minuteCounter = 0
  
  
  def sendTweet(self, type, message):  
    #try:
      ##OLD TWITTER lib code broken? t = Twitter(auth=OAuth(self.accessToken, self.accessTokenSecret, self.consumerKey, self.consumerSecret))
      ##s = self.livDeviceName +'  '+ type + '   ' + message
      ##t.statuses.update(status=s)
      auths = OAuthHandler(self.consumerKey, self.consumerSecret)
      auths.set_access_token(self.accessToken, self.accessTokenSecret)
      api = tweepy.API(auths)
      s = type + '  ' + message
      api.update_status(status=s)       
      self.logger.info("LiV sent a tweet  " + s)  
    #except Exception as e:
    #  e = sys.exc_info()[0]
    #  self.logger.critical(str(e))
      
  
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
  print "token  " + "   " + str(tm.accessToken)
  print "token secret " + "   " + str(tm.accessTokenSecret)
  print "consumer secret  " + "   " + str(tm.consumerSecret)
  print "consumer key  " + "   " + str(tm.consumerKey)
  
  if tm.alarmActive == True:
    tm.sendTweet("Alarm", "this is an alarm test")
    print "sent alarm tweet"  
    
  
  if tm.reportActive == True:
    tm.sendTweet("Report", "WHASD SLDKJ LSD LKjlk")  
    print "send report tweet"    
  
  
  
  