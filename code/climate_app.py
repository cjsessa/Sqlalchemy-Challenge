# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 16:18:51 2020

@author: adfil
"""

## Step 2 - Climate App

##Now that you have completed your initial analysis, design a Flask API based 
##on the queries that you have just developed.

##* Use FLASK to create your routes.

### imports
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#######################
#Database Setup
########################


#creating linke to sql data
#creating our session link from Python to the DB
#reflect existing database into new model
#reflect the tables
#save reference to table
engine = create_engine("sqlite:///../data/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True) 
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#merging into one large file
merge = engine.execute('select a.ID, a.station, a.date,a.prcp,a.tobs,b.name,b.latitude,b.longitude,b.elevation from Measurement as a join Station as b on a.station = b.station and a.id = b.station;').fetchall()


#jsonify

 #######################
#creating app
#######################

app = Flask(__name__)

 ## Home page.
@app.route("/")
def home():
    ##List all routes that are available.
    ##`/api/v1.0/precipitation`
    return(
        f"Hawaii Climite Analysis Routes:<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Tobs</a><br/>"
        f"<a href='/api/v1.0/temp/start/end'>Start & End Date</a><br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Calculate the date 1 year ago from the last data point in the database
    #last date in dataset 2017-08-23
    last_date = session.query(Measurement.date).\
               filter(func.strftime(Measurement.date)).\
               order_by(Measurement.date.desc()).first()
    
    vac=last_date[0].split('-')
    last_year = dt.date(int(vac[0]),int(vac[1]),int(vac[2]))-dt.timedelta(days = 365)

    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    precip = list(np.ravel(precipitation))
    return jsonify(precip)
    
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()  
    stat = list(np.ravel(stations))
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).\
              filter(func.strftime(Measurement.date)).\
              order_by(Measurement.date.desc()).first()
    
    vac=last_date[0].split('-')
    last_year = dt.date(int(vac[0]),int(vac[1]),int(vac[2]))-dt.timedelta(days = 365)

    tob = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()
    tobs = [{tobs[0]:tobs[1]} for tobs in tob]
    # tobs = {date:tob for date, tobs in tob}
    return jsonify(tobs)

@app.route("/api/v1.0/temp/<start>/<end>")

def date_range(start=None,end=None):
    
    start = '2016-01-01'
    end = '2016-01-15'
    
    if end:
        rng = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        rng = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    return jsonify(rng)
    
if __name__ == '__main__':
    app.run()
    
    