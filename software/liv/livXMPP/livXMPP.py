'''
Created by alfredc333
First Cypress Limited, 2015
MIT license
'''

import sys,os,xmpp,time
import threading
import ConfigParser
import logging
import logging.config
from commandManager import commandManager
import smtplib
from email.mime.text import MIMEText as text

from twitter import *
import httplib2 as http
import json
from urlparse import urlparse
from emailManager import *
from twitterManager import *
 
 
class xmppLiv:

  def __init__(self, j, p, rjid, emailManager, twitterManager, log, cm):
    self.jabber = j
    self.password = p
    self.remotejid = rjid
    
    #self.keepAliveTime = kaTime
    self.logger = log
    self.commandManager = cm
    
    self.eManager = emailManager
    self.tManager = twitterManager
    
     
  def registerHandlers(self):
    self.logger.info('Register Handlers')
    self.jabber.RegisterHandler('message',self.xmppProcessMessage)

  def xmppProcessMessage(self, con, event):
    self.logger.info('Start processing XMPP message ')
    type = event.getType()
    fromjid = event.getFrom().getStripped()
    body = event.getBody()
    if type in ['message', 'chat', None] and fromjid == self.remotejid and body:
      self.logger.info('Reply to message: ' + body)
      self.respondMessage(body)

  def xmppKeepAlive(self, c):
    while True:
      #print("Start xmppKeepAlive thread")

      #KEEP ALIVE TIME is 60 seconds.
      #DO NOT MODIFY this value unless you understand how this will impact sending alerts and 
      #reports via XMPP, email and twitter!!!  
      time.sleep(60)      
      
      #send XMPP presence info to keep connection alive 
      pres = xmpp.Presence()
      pres.setStatus("LIV IS AVAILABLE")
      self.jabber.send(pres)
      
      #send email report if configured and the time to report is now
      if self.eManager.getEmailReportFlag() == True:
        self.eManager.incrementMinuteCounter()
        self.logger.info("eManager timer incremented")  
        if self.eManager.sendEmailReportNow() == True:
          m = self.getMeasurements()      
          self.eManager.sendEmail("LiV Report ", m)
          self.eManager.resetMinuteCounter()
      
      #send twitter report if configured and the time to report is now
      if self.tManager.getTwitterReportFlag() == True:
        self.tManager.incrementMinuteCounter()
        self.logger.info("tManager timer incremented")  
        if self.tManager.sendTwitterReportNow() == True:
          m = self.getMeasurements()      
          self.tManager.sendTweet("Report: ", m)
          self.tManager.resetMinuteCounter()
          
          
      #send XMPP alarm notification if needed
      msgList = self.commandManager.checkAlarms()
      for i in msgList:
        m = xmpp.protocol.Message(to=self.remotejid, body=i, typ='chat')
        self.jabber.send(m)
        
        #send email alarm notification
        if self.eManager.getEmailAlertFlag() == True:
          self.logger.info("Sending email alert  "  + i)   
          self.eManager.sendEmail("LiV Pi Alarm Notification", i)
           
        #send twitter notification
        if self.tManager.getTwitterAlarmFlag() == True:
           self.logger.info("Sending twitter alert " + i)
           self.tManager.sendTweet("Alarm: ", i)
           
           
  def xmppConnect(self):
    con=self.jabber.connect()
    if not con:
      self.logger.critical('XMPP FAILED TO CONNECT')
      return False
    #sys.stderr.write('connected with %s\n'%con)
    auth=self.jabber.auth(jid.getNode(),self.password,resource=jid.getResource())
    if not auth:
      self.logger.critical('XMPP FAILED TO AUTHENTICATE')
      return False
    pres = xmpp.Presence()
    pres.setStatus("LIV IS AVAILABLE")
    self.jabber.send(pres)
    self.registerHandlers()
    return con

  def respondMessage(self, c):
    self.logger.info('Starting to respond to XMPP message')
    message = 'empty'
    message = self.commandManager.processCommand(c)
    m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
    self.jabber.send(m)
    
  def getMeasurements(self):
    target = urlparse("http://localhost:5000/getAllRawSensorData")
    method = 'GET'
    body = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    h = http.Http()
    response, content = h.request(target.geturl(), method, body, headers)
       
    # assume that content is a json reply
    data = json.loads(content)
    #print("data is ")
    #print(data)
       
    #measurements
       
    m = ( 'TEMPERATURE=' + data['Temperature'] + 'C ' + \
           'HUMIDITY=' + data['Humidity'] + '% ' + \
           'AIR PRESSURE=' + data['AirPressure'] +'hPa ' + \
           'CO2 LEVEL=' + data['CO2level'] +'ppm ' + \
           'TIME STAMP = ' + data['Timestamp'])
    return m


  '''
  def sendTwitter(self, token, token_key, con_secret, con_secret_key, data):
      print "send twitter"
  '''
    
if __name__ == '__main__':

  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  
  
  
  config = ConfigParser.ConfigParser()
  config.read("./livXMPP.config")
  xmppFrom = config.get('XMPP', 'from')
  xmppFromPassword = config.get('XMPP', 'from_password')
  xmppTo = config.get('XMPP', 'to')

  apiURLdata = config.get('API', 'url_raw_sensor_data')
  apiURLbase = config.get('API', 'url_base')

  config.read("../livDB/livDB.config")
  tempFormat = config.get('FORMAT','temperature') 
  airPressureFormat = config.get('FORMAT','airpressure')

  emailMgr = emailManager(logger)
  
  twitterMgr = twitterManager(logger)

  jid=xmpp.protocol.JID(xmppFrom)
  client=xmpp.Client(jid.getDomain(),debug=[])
  
  cm = commandManager(logger, apiURLdata, apiURLbase, './livXMPP.config', tempFormat, airPressureFormat)
  

  bot=xmppLiv(client, xmppFromPassword, xmppTo, emailMgr, twitterMgr, logger, cm)
  
  '''
  print bot.eAlarmActive
  print bot.eServer
  print bot.eFrom
  print bot.eFromPassword
  print bot.eTo
  exit()
  '''
    
  '''
  if not bot.xmppConnect():
    logger.error('Could not connect to server, or password mismatch!\n')
    sys.exit(1)
  else:
    logger.info('Successful XMPP Connection\n')
    #client.sendInitPresence()
  ''' 

  try: 
    while (not bot.xmppConnect()):      
      #try again connection after 300 seconds
      time.sleep(60)
  except:
    logger.error('Could not connect to server, or password mismatch!\n')   
    sys.exit(1)
     
  logger.info('Successful XMPP Connection\n')
    
  try:
    keepalive_th = threading.Thread(target=bot.xmppKeepAlive, args =(client,) )
    keepalive_th.setDaemon(True)
    keepalive_th.start()
    logger.info('Keep alive thread started')
  except:
    logger.error('Failed to start keep alive thread. Stop XMPP process')  
    sys.exit(1) 

  while 1:
    try:  
      client.Process(1)    
    except: 
      logger.error('Critical error. Stop XMPP process')  
      sys.exit(1)

