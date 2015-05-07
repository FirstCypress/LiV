'''
Created by alfredc333
First Cypress Limited, 2014
MIT license
'''


import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, send_file
import time
from time import gmtime, strftime, localtime 
import logging
import logging.config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import *
from optparse import OptionParser
import StringIO


app = Flask(__name__, instance_path='/home/pi/liv/livAPIs')

logging.config.fileConfig('livAPIsLogging.ini')
app.logger_name = logging.getLogger(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../livDB/liv.db'),
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


def getData(recs):
    timeStamp = strftime("%Y-%m-%d %H:%M:%S")
    app.logger_name.debug('Starting DB retrieval at ' + timeStamp)
    db = get_db()
    query = 'SELECT * from Measurements ORDER By Mid DESC LIMIT ' + str(recs)
    cur = db.execute(query)
    rows = cur.fetchall()
    return rows


  
def prepareData(dbRecName, numberRecords):
    records = getData(int(numberRecords))
    m = []
    x = []
    l = records[0]
    f = records[-1]
    fromTS = f["Timestamp"]
    toTS = l["Timestamp"]
    i = 0
    for record in records[::-1]:
      m.append(record[dbRecName])
      x.append(i)
      i = i + 1
    return fromTS, toTS, x, m
    
  


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def getInfo():
    return 'Available APIs: .../getAllSensorData   .../getSystemDate'



@app.route('/newliv')
def newliv():
      app.logger_name.debug('Access /newliv web page')
      records = getData(1)
      c = records[0]
      t = c["Temperature"]
      h = c["Humidity"]
      ap = c["AirPressure"]
      ts = c["Timestamp"]
      co2 = c["CO2level"]
      sData = { 'Temperature': t, 'Humidity': h, 'AirPressure': ap, 'Timestamp': ts, 'CO2level': co2} 
      return render_template('livHomePage.html', sensorData=sData)

@app.route('/liv')
def liv():
    app.logger_name.debug('Access /liv web page')
    records = getData(1)
    c = records[0]
    t = c["Temperature"]
    h = c["Humidity"]
    ap = c["AirPressure"]
    ts = c["Timestamp"]
    co2 = c["CO2level"]
    sData = { 'Temperature': t, 'Humidity': h, 'AirPressure': ap, 'Timestamp': ts, 'CO2level': co2} 
    return render_template('liv.html', sensorData=sData)
    

@app.route('/getAllSensorData')
def getAllSensorDataFromMostRecentReading():
    print "start getAllSensorData"
    records = getData(1)
    c = records[0]
    t = c["Temperature"]
    h = c["Humidity"]
    ap = c["AirPressure"]
    ts = c["Timestamp"]
    co2 = c["CO2level"]
    return jsonify({ 'Temperature': str(t) + ' C', 'Humidity': str(h) + ' %', 'AirPressure': str(ap) + ' hPa', 'Timestamp': ts, 'CO2level': str(co2) + ' ppm'})


@app.route('/getSystemDate', methods=['GET'])
def getSystemDate():
  timestamp = strftime("%Y-%m-%d %H:%M:%S")
  return jsonify({ 'LiV Date': timestamp })

# use POST for setting date, this is just for browser testing.
@app.route('/setHongKongDate', methods=['GET'])
def setHongKongDate():
  os.environ['TZ'] = 'Hongkong'
  time.tzset()
  timestamp = strftime("%Y-%m-%d %H:%M:%S")
  return jsonify({ 'LiV Date set to': timestamp })

@app.route('/co2/<numberRecords>')
def images(numberRecords):
    return render_template("CO2.html", title=numberRecords)

@app.route('/CO2Fig/<numberRecords>')
def CO2Fig(numberRecords):
    fromTS, toTS, x, m = prepareData("CO2level", numberRecords)
    
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_bgcolor("#ffff00")
    plt.ylabel("CO2 Level in PPM")
    plt.title("From: " + fromTS + "                            To: " + toTS)
    plt.xlabel('Number of measurement points ')
    ax.plot(x, m, color='#009900')
    
    img = StringIO.StringIO()
    # plt.savefig('co2.png')
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/temperature/<numberRecords>')
def tGraph(numberRecords):
    return render_template("temperature.html", title=numberRecords)

@app.route('/tFig/<numberRecords>')
def tFig(numberRecords):
    fromTS, toTS, x, m = prepareData("Temperature", numberRecords)
    
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_bgcolor("#ffff00")
    plt.ylabel("Temperature in C degrees")
    plt.title("From: " + fromTS + "                            To: " + toTS)
    plt.xlabel('Number of measurement points ')
    ax.plot(x, m, color='#009900')
    
    img = StringIO.StringIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/humidity/<numberRecords>')
def hGraph(numberRecords):
    return render_template("humidity.html", title=numberRecords)

@app.route('/hFig/<numberRecords>')
def hFig(numberRecords):
    fromTS, toTS, x, m = prepareData("Humidity", numberRecords)
    
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_bgcolor("#ffff00")
    plt.ylabel("Humidity in %")
    plt.title("From: " + fromTS + "                            To: " + toTS)
    plt.xlabel('Number of measurement points ')
    ax.plot(x, m, color='#009900')
    
    img = StringIO.StringIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/airPressure/<numberRecords>')
def apGraph(numberRecords):
    return render_template("airPressure.html", title=numberRecords)

@app.route('/apFig/<numberRecords>')
def apFig(numberRecords):
    fromTS, toTS, x, m = prepareData("AirPressure", numberRecords)
    
    plt.clf()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_bgcolor("#ffff00")
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.ylabel("Air Pressure in hPa")
    plt.title("From: " + fromTS + "                            To: " + toTS)
    plt.xlabel('Number of measurement points ')
    ax.plot(x, m, color='#009900')
    
    img = StringIO.StringIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':

  # app.run(host='0.0.0.0', debug = True)
#   logging.config.fileConfig('livAPIsLogging.ini')
#   app.logger_name = logging.getLogger(__name__)
  # app.debug = True

  app.run('0.0.0.0', debug=False)
    
