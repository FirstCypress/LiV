#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set et tabstop=4 shiftwidth=4 nu nowrap fileencoding=utf-8:
#
# Raspberry Pi example
#



import sys
import os
import threading
from ConfigParser import ConfigParser
from time import sleep


from twisted.python import log
from twisted.internet import reactor
from zope.interface import implements

try:
    import devicehive
except :
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import devicehive
import devicehive.interfaces
import devicehive.auto

import httplib2 as http
import json
from urlparse import urlparse


class RPiDescr( devicehive.DeviceInfo ):

    """
    This class describe a raspberry pi virtual device.
    """

    implements(devicehive.IDeviceInfo)

    def __init__(self):

        super(RPiDescr, self).__init__(name = 'LiV Device',
                                       status = 'Online',
                                       network = devicehive.Network(key = 'yourKeyHere',
                                       name = 'LiV Network',
                                       descr = 'LiV Air Monitoring Network'),
                                       device_class = devicehive.DeviceClass(name = 'LiV',
                                       version = '1.0'),
                                       equipment = [devicehive.Equipment(name = 'K30', code = 'CO2s', type = 'CO2 sensor'),
                                       devicehive.Equipment(name = 'DHT22', code = 'temp', type = 'Temperature Sensor'),
                                       devicehive.Equipment(name = 'DHT22', code = 'hum', type = 'Humidity Sensor'),
                                       devicehive.Equipment(name = 'BMP170', code = 'ap', type = 'Air Pressure Sensor')])
        pass

class BaseRPiApp(object):

    implements(devicehive.interfaces.IProtoHandler)
    factory = None
    info = RPiDescr()
    def on_apimeta(self, websocket_server, server_time):
        pass

    def on_connected(self):
        pass

    def on_connection_failed(self, reason) :
        pass

    def on_closing_connection(self):
        pass

    def on_failure(self, device_id, reason):
        pass

    def on_command(self, device_id, command, finished):
        raise NotImplementedError('You need to override base abstract method.')

    def notify(self, notification, **params):
        if self.factory is not None :
            self.factory.notify(notification, params, self.info.id, self.info.key)

class RPiApp(BaseRPiApp) :
    def __init__(self):
        super(RPiApp, self).__init__()
        self.last_temperature = None
        self.last_humidity = None
        self.last_airPreassure = None
        self.last_CO2 = None

    def initialize(self, config_file_path):
        self.init_config(config_file_path)

    def init_config(self, config_file_path):
        conf = ConfigParser()
        conf.read(config_file_path)
        self.info.id = conf.get('device', 'id')
        self.info.key = conf.get('device', 'key')

    def on_connected(self):
        """
        Register one or more devices right after library
        has connected todevice-hive server.
        """
        def on_subscribe(result) :
            """
            After device has registered in device-hive server it
            sends temperature update notification. And then it starts listening for a command.
            """
            self.update_readings()
            self.factory.subscribe(self.info.id, self.info.key)

        def on_failed(reason) :
            log.err('Failed to save device {0}. Reason: {1}.'.format(self.info, reason))

        self.factory.device_save(self.info).addCallbacks(on_subscribe, on_failed)

    
# DATA PUSH 
    def update_readings(self):
        target = urlparse('http://localhost:5000/getAllSensorData')
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
        
            
        self.last_temperature = data['Temperature']
        self.last_airPressure = data['AirPressure']
        self.last_humidity = data['Humidity']
        self.last_CO2 = data['CO2level']
        self.notify('equipment', equipment = 'temp', temperature = self.last_temperature)
        self.notify('equipment', equipment = 'hum', humidity = self.last_humidity)
        self.notify('equipment', equipment = 'ap', airPressure = self.last_airPressure)
        self.notify('equipment', equipment = 'CO2s', CO2 = self.last_CO2)
        
        #update every 300 sec
        reactor.callLater(300.0, self.update_readings)
    

    def need_to_notify(self, temperature):
        if self.last_temperature is None :
            return True
        return abs(temperature - self.last_temperature) > 0.2


    def on_command(self, device_id, command, finished):
        cmd_name = command.command
        cmd_params = command.parameters
        if cmd_name == 'UpdateLedState' :
            equipment = cmd_params['equipment']
            state = cmd_params['state']
            log.msg("<{0}> -> {1}.".format(equipment, state))
            finished.calback(devicehive.CommandResult('Completed', 'OK'))
        else :
            finished.errback(NotImplementedError('Unknown command: <{0}> ignored.'.format(cmd_name)))


def config_file_name():
    return os.path.join(os.path.dirname(__file__), os.path.splitext(os.path.basename(__file__))[0] + '.cfg')


if __name__ == '__main__' :

    # 0.
    log.startLogging(sys.stdout)

    # 1.
    rpi_app = RPiApp()
    rpi_app.initialize(config_file_name())

    # 2.

    factory = devicehive.auto.AutoFactory(rpi_app)

    # 3.
    # factory.connect("http://pg.devicehive.com/api/")
    factory.connect("http://nn7956.pg.devicehive.com/api/")

    reactor.run()



