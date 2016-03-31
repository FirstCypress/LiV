import sys
import ConfigParser
import logging
import logging.config
import smtplib
from email.mime.text import MIMEText as text

class  emailManager:

  def  __init__(self, log ):
    self.logger = log
    config = ConfigParser.ConfigParser()
    config.read("./email.config")
  
    self.livDeviceName = config.get('EMAIL', 'liv_device_name')
    self.eAlarm = config.getboolean('EMAIL', 'email_alarm_active')
    self.eReport = config.getboolean('EMAIL', 'email_report_active')
    self.eReportTime = config.getint('EMAIL', 'email_report_time')
    self.eServer = config.get('EMAIL', 'email_server')
    self.eFrom = config.get('EMAIL', 'from')
    self.eFromPassword = config.get('EMAIL', 'from_password')
    self.eToList = config.get('EMAIL', 'toList')
    self.minuteCounter = 0
  
  
  def sendEmail(self, subject, message):
    try:  
      server = smtplib.SMTP(self.eServer)
      server.starttls()
      server.login(self.eFrom, self.eFromPassword)
      eMsg = text("FROM " + self.livDeviceName +"\n" + "\n" + "\n" + message)
      eMsg['Subject'] = subject      
      eMsg['From'] = self.eFrom
      eMsg['To'] = self.eToList
      server.sendmail(self.eFrom, self.eToList.split(','), eMsg.as_string())
      server.quit()
      self.logger.info("LiV email sent")
    except:
      e = sys.exc_info()[0]
      self.logger.critical(e)  
  
  
  def getEmailAlertFlag(self):
    return self.eAlarm
  
  def sendEmailReportNow(self):
    if self.minuteCounter == self.eReportTime:  
      return True
    else:
      return False      
          
  def getEmailReportFlag(self):
    return self.eReport  
      
  
  def incrementMinuteCounter(self):
      self.minuteCounter +=1
  
  
  def resetMinuteCounter(self):
      self.minuteCounter = 0  

    
if __name__ == "__main__":
  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  
  em = emailManager(logger)
  print "emailAlarmFlag" + "   " + str(em.eAlarm)
  print "emailReportFlag" + "   " + str(em.eReport)
  print "emailFrom" + "   " + em.eFrom
  print "emailFromPasswd" + "   " + em.eFromPassword
  print "emailToList" + "   " + em.eToList
  print "emailServer" + "   " + em.eServer
  
  
  if em.eAlarm == True:
    em.sendEmail("LiV Alarm Notification", "here is the alarm")
  
  if em.eReport == True:  
    em.sendEmail("LiV Report", "here is the report")
  
  
  
  
  