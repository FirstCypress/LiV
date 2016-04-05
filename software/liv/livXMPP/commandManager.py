import ConfigParser
import time
import httplib2 as http
import json
from urlparse import urlparse
import logging
import logging.config
import socket 
import stun


class  commandManager:

  def  __init__(self, log, auData, auBase, path, temperatureFormat='C', airPressureFormat='hPa'):
    self.config = ConfigParser.RawConfigParser()
    self.logger = log
    self.apiURLdata = auData
    self.apiURLbase = auBase
    self.tFormat = temperatureFormat
    self.apFormat = airPressureFormat
    self.path = path
    self.config.read(path)
    self.parameter0 = ['report', 'website','set','reset','alarms','show']
    self.parameter1 = ['temperature','humidity','airpressure', 'co2']
    self.parameter2 = ['more','less']
    self.alarmFlags = {'temperature' :False, 'humidity': False, 'airpressure': False, 'co2': False}
    self.alarmWasSent  = {'temperature' :False, 'humidity': False, 'airpressure': False, 'co2': False}
    self.alarmCompRules  = {'temperature' :'more', 'humidity': 'more', 'airpressure': 'more', 'co2': 'more'}
    self.alarmValues  = {'temperature' : 9999, 'humidity': 9999, 'airpressure': 9999, 'co2': 9999}

  def retrieveLastMeasurementsJSON(self):
    #url="http://localhost:5000/getAllRawSensorData"
    #uri = 'http://yourservice.com'
    #path = '/path/to/resource/'
    target = urlparse(self.apiURLdata)
    self.logger.info(target)
    method = 'GET'
    body = ''
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
    }

    h = http.Http()
# If you need authentication:
#    h.add_credentials(auth.user, auth.password)

    #self.logger.info("before request")
    response, content = h.request(target.geturl(), method, body, headers)
    #self.logger.info("after request")
    
# assume that content is a json reply
    data = json.loads(content)
    return data 
  


  def retrieveLastMeasurements(self):
    
    data = self.retrieveLastMeasurementsJSON()
                                         
    
    m = ('Measurements from LIV: \n' + \
         'TEMPERATURE = ' + data['Temperature'] + ' ' + self.tFormat +' \n' + \
        'HUMIDITY = ' + data['Humidity'] + ' %'+ ' \n' + \
         'AIR PRESSURE = ' + data['AirPressure'] + ' ' + self.apFormat + '\n' + \
         'CO2 LEVEL = ' + data['CO2level'] +' ppm' + '\n' + \
         'TIME STAMP = ' + data['Timestamp'])
    return m


  def findIPAddress(self):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #connect to google to get local IP address
      s.connect(("8.8.8.8",80))
      ip = s.getsockname()[0]
      s.close()
      return ip, True
    except:
      ip = "Error: unable to retrieve local IP address"
    return ip, False;


  def findExternalIPAddress(self):
    try:
      nat_type, external_ip, external_port = stun.get_ip_info(stun_port=3478)      
      return external_ip, True
    except:
      eip = "Error: unable to retrieve local IP address"
    return eip, False;


  def retrieveLivAddress(self):
    l1 = "ERROR: unable to find LiV's IP address"
    l2 = "ERROR: unable to find LiV's External IP address"
      
    IP,f1 = self.findIPAddress()
    eIP,f2 = self.findExternalIPAddress()
    
    if f1==True:
      l1 = self.apiURLbase.replace('localhost', IP) + 'newliv'
    
    if f2==True:
      l2 = l2 = self.apiURLbase.replace('localhost', eIP) + 'newliv'
      
    m = 'INTRANET:\n' + l1 + '\n\n\n' + 'EXTERNAL:\n' + l2
    return m
    

  def retrieveMeasurementsAddress(self, c):
    l1 = "ERROR: unable to find LiV's IP address"
    l2 = "ERROR: unable to find LiV's External IP address"
    m = ''
    if len(c) < 3:
      m = 'There should be two parameters in set command: '
      return m
    
    for i in self.parameter1:
      if c[1] == i:
        try:
          int(c[2])
        except:
          m = 'third parameter should be integer'
          break
        IP, f1 = self.findIPAddress()
        eIP,f2 = self.findExternalIPAddress()
        
        if f1==True:
          l1 = self.apiURLbase.replace('localhost', IP) + c[1] +'/' + c[2]
        if f2==True:
          l2 = self.apiURLbase.replace('localhost', eIP) + c[1] +'/' + c[2]
          
        m = 'INTRANET:\n' + l1 + '\n\n\n' + 'EXTERNAL:\n' + l2
        break
      else:
        m ='invalid first parameter'
    return m

  def setAlarm (self, c):
    #check if enough parameters
    
    if len(c) < 4:
      m = 'There should be three parameters in set command: '
      return m
      
    self.config.read(self.path)
    
    for i in self.parameter1:
      if c[1] == i:
        for n in self.parameter2:
          if c[2] == n:
            try:
              float(c[3])
            except:
              m ="Failed to set alarm. Invalid 3d parameter in command: "
              return m
            
            self.config.set(c[1], 'rule', c[2] + ' ' + c[3])
            with open(self.path, 'wb') as configfile:
              self.config.write(configfile)
            m ="Set alarm successfull for command: "
            self.alarmWasSent[i] = False
            return m;
         
        m = "Failed to set alarm. Invalid 2nd parameter in command: "
        return m;
    
    m = "Failed to set alarm. Invalid 1st parameter in command: "
    return m
    
    
  def resetAlarm (self, c):
    if len(c) < 2:
      m = 'There should be one parameter in reset command: '
      return m
      
    self.config.read(self.path)
    for i in self.parameter1:
      if c[1] == i:
        self.config.set(c[1], 'rule', c[0])
        with open(self.path, 'wb') as configfile:
          self.config.write(configfile)
        m = "Alarm reset successful for command: "  
        self.alarmWasSent[i] = False
        return m
      elif c[1] == 'all':
        
        self.config.set(self.parameter1[0] ,'rule', c[0])
        self.config.set(self.parameter1[1] ,'rule', c[0])
        self.config.set(self.parameter1[2] ,'rule', c[0])
        self.config.set(self.parameter1[3] ,'rule', c[0])
        with open(self.path, 'wb') as configfile:
          self.config.write(configfile)
        m ='alarm reset succesful for commad: '
        return m
        
    m = "Failed to reset alarm. Invalid parameter in command: "
    return m
  
  def reportAlarms(self):
    self.config.read(self.path)
    m = 'alarm rules: \n' +'   \n'
    for i in self.parameter1:
      rule = self.config.get(i, 'rule')
      #print i + '   ' + rule
      m+= i + ':   ' + rule + ';\n'
    
    return m  
  
  def readAlarmStatus(self):
    self.config.read(self.path)
    
    for i in self.parameter1:
      rule = self.config.get(i, 'rule')
      #print i + '   ' + rule
      r = rule.lower().split(' ')
      if r[0] == 'reset':
        self.alarmFlags[i] = False
      else:
        self.alarmFlags[i] = True
        self.alarmCompRules[i] = r[0]
        self.alarmValues[i] = r[1]
  
  def  checkAlarms (self):
    messageList =[]
    alarmFlag = False
    
    self.readAlarmStatus()
    
    
    for i, v in self.alarmFlags.iteritems():
      if v == True:
        alarmFlag = True
        break
        
    if alarmFlag == False:
      return messageList
    else:
      data = self.retrieveLastMeasurementsJSON()
      #some nasty kludge here, should fix names in database instead of name mapping !!!
      d = {'temperature': data['Temperature'], 'humidity': data['Humidity'], 'airpressure': data['AirPressure'], 'co2': data['CO2level']}
      
      #print 'GOT latest msrmnts'
      for i, v in self.alarmFlags.iteritems():
        #print i, v
        if v == True:
          #print 'check'
          if self.alarmCompRules[i] == 'more':
            #print d[i]
            #print self.alarmValues[i]
            alarmMessage = '\nThreshold is ' + self.alarmValues[i] + '\nCurrent value of ' + i +' is ' +d[i] \
                                      +  '\nTimestamp:  ' + data['Timestamp']
            if float(d[i]) > float(self.alarmValues[i]):
              if self.alarmWasSent[i] == False:
                messageList.append( i + ' ALARM NOTIFICATION!' + alarmMessage)
                self.alarmWasSent[i] = True
            else:
              if self.alarmWasSent[i] == True:
                messageList.append( i + ' CLEAR ALARM NOTIFICATION!'  + alarmMessage)
                self.alarmWasSent[i] = False
          elif self.alarmCompRules[i] == 'less':
            #print d[i]
            #print self.alarmValues[i]
            if float(d[i]) < float(self.alarmValues[i]):
              if self.alarmWasSent[i] == False:
                messageList.append( i + ' ALARM NOTIFICATION!' + alarmMessage)
                self.alarmWasSent[i] = True
            else:
              if self.alarmWasSent[i] == True:
                messageList.append( i + ' CLEAR ALARM NOTIFICATION!' + alarmMessage)
                self.alarmWasSent[i] = False
          else:
            #this should never happen
            messageList.append('ERROR checking alarms levels')  
    return messageList
      

  

  def processCommand(self, command):
    c = command.lower().split(' ')
    
    #report
    if self.parameter0[0] == c[0]:
      message = self.retrieveLastMeasurements()
    #website
    elif self.parameter0[1] == c[0]:
      message = self.retrieveLivAddress()
    #set
    elif self.parameter0[2] == c[0]:
      msg = self.setAlarm(c)
      message = msg + command
    #reset
    elif self.parameter0[3] == c[0]:
      msg = self.resetAlarm(c)
      message = msg + command
    #alarms
    elif self.parameter0[4] == c[0]:
      msg = self.reportAlarms()
      message = msg
    #show 
    elif self.parameter0[5] == c[0]:
      msg = self.retrieveMeasurementsAddress(c)
      message = msg
    else:
      message = 'Command    ' + command + '   is not supported' 
      
    return message
    
    

#
if __name__ == "__main__":

  logging.config.fileConfig('livXMPPLogging.ini')
  logger = logging.getLogger(__name__)  


  config = ConfigParser.ConfigParser()
  config.read("./livXMPP.config")
  apiURLdata = config.get('API', 'url_raw_sensor_data')
  apiURLbase = config.get('API', 'url_base')
  cm = commandManager(logger, apiURLdata, apiURLbase,"./livXMPP.config")
  
  m = cm.retrieveLivAddress()
  print m
  print '------------'
  m = cm.retrieveLastMeasurements()
  print m
  print '--------------'
  cm.readAlarmStatus()
  for i, v in cm.alarmFlags.iteritems():      
    print i,v 
  print '--------------'
  for i, v in cm.alarmCompRules.iteritems():      
    print i,v 
  print '--------------'
  for i, v in cm.alarmValues.iteritems():      
    print i,v   
  print '--------------'
    
  ml = cm.checkAlarms()
  for i in ml:
    print i


