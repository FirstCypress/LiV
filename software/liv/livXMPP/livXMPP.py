'''
Created by alfredc333
First Cypress Limited, 2015
MIT license
'''

import sys,os,xmpp,time
import threading
import httplib2 as http
import json
from urlparse import urlparse
import ConfigParser
import logging
import logging.config


class xmppLiv:

  def __init__(self, j, p, rjid, apiUrl, log, kaTime=60):
    self.jabber = j
    self.password = p
    self.remotejid = rjid
    self.APIurl = apiUrl
    self.keepAliveTime = kaTime
    self.logger = log

  def registerHandlers(self):
    self.logger.debug('Register Handlers')
    self.jabber.RegisterHandler('message',self.xmppProcessMessage)

  def xmppProcessMessage(self, con, event):
    self.logger.debug('Start processing XMPP message ')
    type = event.getType()
    fromjid = event.getFrom().getStripped()
    body = event.getBody()
    if type in ['message', 'chat', None] and fromjid == self.remotejid and body:
      self.logger.debug('Reply to message: ' + body)
      self.respondMessage(body)

  def xmppKeepAlive(self, c):
    while True:
      time.sleep(self.keepAliveTime)
      pres = xmpp.Presence()
      pres.setStatus("LIV IS AVAILABLE")
      self.jabber.send(pres)

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

  def respondMessage(self, b):
    self.logger.info('Starting to respond to XMPP message')
    message = 'empty'
    #Report command is only command supported
    if 'report'.lower() in b.lower():
      message = self.retrieveMeasurements()
    else:
      message = 'Command ' + b + ' is not supported'
    m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
    self.jabber.send(m)


  def retrieveMeasurements(self):
    #url="http://localhost:5000/getAllSensorData"
    #uri = 'http://yourservice.com'
    #path = '/path/to/resource/'
    target = urlparse(self.APIurl)
    method = 'GET'
    body = ''
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
    }

    h = http.Http()
# If you need authentication:
#    h.add_credentials(auth.user, auth.password)

    response, content = h.request(target.geturl(), method, body, headers)

# assume that content is a json reply
    data = json.loads(content)
    r = ('Measurements from LIV: \n' + \
         'TEMPERATURE = ' + data['Temperature'] + '\n' + \
        'HUMIDITY = ' + data['Humidity'] + '\n' + \
         'AIR PRESSURE = ' + data['AirPressure'] +'\n' + \
         'CO2 LEVEL = ' + data['CO2level'] +'\n' + \
         'TIME STAMP = ' + data['Timestamp'])
    return r

    
if __name__ == '__main__':

  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  
  
  
  config = ConfigParser.ConfigParser()
  config.read("./livXMPP.config")
  xmppFrom = config.get('XMPP', 'from')
  xmppFromPassword = config.get('XMPP', 'fromPassword')
  xmppTo = config.get('XMPP', 'to')
  xmppKeepAliveTime = config.getint('XMPP', 'keepAliveTime')
  apiURL = config.get('API', 'url')

  
  jid=xmpp.protocol.JID(xmppFrom)
  client=xmpp.Client(jid.getDomain(),debug=[])
  bot=xmppLiv(client, xmppFromPassword, xmppTo, apiURL, logger, xmppKeepAliveTime)

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


