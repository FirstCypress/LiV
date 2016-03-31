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

class xmppLiv:

  def __init__(self, j, p, rjid, emAlarm, emServer, emFrom, emFromPassword, emTo, log, cm, kaTime=60):
    self.jabber = j
    self.password = p
    self.remotejid = rjid
    
    self.keepAliveTime = kaTime
    self.logger = log
    self.commandManager = cm
    
    self.eAlarmActive = emAlarm
    self.eServer = emServer
    self.eFrom = emFrom
    self.eFromPassword = emFromPassword
    self.eTo = emTo
    
    

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
      time.sleep(self.keepAliveTime)
      pres = xmpp.Presence()
      pres.setStatus("LIV IS AVAILABLE")
      self.jabber.send(pres)
      #send alarm notification if needed
      msgList = self.commandManager.checkAlarms()
      for i in msgList:
        m = xmpp.protocol.Message(to=self.remotejid, body=i, typ='chat')
        self.jabber.send(m)
        #send email notification
        if self.eAlarmActive == True:
          try:  
            server = smtplib.SMTP(self.eServer)
            server.starttls()
            server.login(self.eFrom, self.eFromPassword)
            eMsg = text(i)
            eMsg['Subject'] = 'LiV Pi notification'
            eMsg['From'] = self.eFrom
            eMsg['To'] = self.eTo

            server.sendmail(self.eFrom, self.eTo, eMsg.as_string())
            server.quit()
          except:
            e = sys.exc_info()[0]
            self.logger.critical(e)  

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

  

    
if __name__ == '__main__':

  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  
  
  
  config = ConfigParser.ConfigParser()
  config.read("./livXMPP.config")
  xmppFrom = config.get('XMPP', 'from')
  xmppFromPassword = config.get('XMPP', 'from_password')
  xmppTo = config.get('XMPP', 'to')
  xmppKeepAliveTime = config.getint('XMPP', 'keep_alive_time')
  #apiURL = config.get('API', 'url')
  apiURLdata = config.get('API', 'url_raw_sensor_data')
  apiURLbase = config.get('API', 'url_base')

  eAlarm = config.getboolean('EMAIL', 'email_alarm_active')
  eServer = config.get('EMAIL', 'email_server')
  eFrom = config.get('EMAIL', 'from')
  eFromPassword = config.get('EMAIL', 'from_password')
  eTo = config.get('EMAIL', 'to')
  
  
  jid=xmpp.protocol.JID(xmppFrom)
  client=xmpp.Client(jid.getDomain(),debug=[])
  cm = commandManager(logger, apiURLdata, apiURLbase, './livXMPP.config')
  #bot=xmppLiv(client, xmppFromPassword, xmppTo, apiURL, logger, cm, xmppKeepAliveTime)
  bot=xmppLiv(client, xmppFromPassword, xmppTo, eAlarm, eServer, eFrom, eFromPassword, eTo, logger, cm, xmppKeepAliveTime)
  
  '''
  print bot.eAlarmActive
  print bot.eServer
  print bot.eFrom
  print bot.eFromPassword
  print bot.eTo
  exit()
  '''
  
  if not bot.xmppConnect():
    logger.error('Could not connect to server, or password mismatch!\n')
    sys.exit(1)
  else:
    logger.info('Successful XMPP Connection\n')
    #client.sendInitPresence()

  keepalive_th = threading.Thread(target=bot.xmppKeepAlive, args =(client,) )
  keepalive_th.setDaemon(True)
  keepalive_th.start()
  logger.info('Keep alive thread started')


  while 1:
    client.Process(1)    


