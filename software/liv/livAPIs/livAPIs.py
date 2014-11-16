'''
Created by alfredc333
First Cypress Limited, 2014
MIT license
'''

import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

import time
from time import gmtime, strftime, localtime 


#app = Flask(__name__)
app = Flask(__name__, instance_path='/home/pi/liv/livAPIs')

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../liv.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def getInfo():
    return 'Available commands: /getAllSensorData /getTemperature /getHumidity /getAirPressure \
    /getCO2level /getSystemDate'

@app.route('/liv')
def liv():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    c= cur.fetchone()
    t = str(c["Temperature"])
    h = c["Humidity"]
    ap = c["AirPressure"]
    ts = c["Timestamp"]
    co2 = c["CO2level"]
    sensorData = { 'Temperature': t, 'Humidity': h, 'AirPressure': ap, 'Timestamp': ts, 'CO2level': co2} 
    return render_template('liv.html', sensorData = sensorData)
    

@app.route('/getAllSensorData')
def getAllSensorDataFromMostRecentReading():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    c= cur.fetchone()
    t = str(c["Temperature"])
    h = c["Humidity"]
    ap = c["AirPressure"]
    ts = c["Timestamp"]
    co2 = c["CO2level"]
    return jsonify( { 'Temperature': t, 'Humidity': h, 'AirPressure': ap, 'Timestamp': ts, 'CO2level': co2} )

@app.route('/getTemperature')
def getLastTemperature():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    id = cur.fetchone()["Temperature"]
    result = str(id)
    return jsonify( { 'Most Recent Temperature Reading ': result } )

@app.route('/getHumidity')
def getLastHumidity():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    id = cur.fetchone()["Humidity"]
    result = str(id)
    return jsonify( { 'Most Recent Humidity Reading ': result } )

@app.route('/getAirPressure')
def getLastAirPressure():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    id = cur.fetchone()["AirPressure"]
    result = str(id)
    return jsonify( { 'Most Recent Air Pressure Reading ': result } )

@app.route('/getCO2level')
def getLastCO2level():
    db = get_db()
    cur = db.execute('SELECT * from Measurements ORDER By Mid DESC LIMIT 1')
    id = cur.fetchone()["CO2level"]
    result = str(id)
    return jsonify( { 'Most Recent CO2 level Reading ': result } )

@app.route('/getSystemDate', methods = ['GET'])
def getSystemDate():
  timestamp = strftime("%Y-%m-%d %H:%M:%S")
  return jsonify( { 'LiV Date': timestamp } )

#use POST for setting date, this is just for browser testing.
@app.route('/setHongKongDate', methods = ['GET'])
def setHongKongDate():
  os.environ['TZ'] = 'Hongkong'
  time.tzset()
  timestamp = strftime("%Y-%m-%d %H:%M:%S")
  return jsonify( { 'LiV Date set to': timestamp } )



if __name__ == '__main__':

  #app.run(host='0.0.0.0', debug = True)
  app.debug = True
  app.run('0.0.0.0')
    