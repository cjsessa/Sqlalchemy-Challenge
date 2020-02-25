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

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)


 ## Home page.
@app.route("/")
def home():
    ##List all routes that are available.
    ##`/api/v1.0/precipitation`
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start&end<br/>"
        f"/api/v1.0/link4<br/>"
        f"/api/v1.0/link5<br/>"
        f"/api/v1.0/link6<br/>"
        f"/api/v1.0/link7<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    ##returning a list
 



  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

* You will need to join the station and measurement tables for some of the analysis queries.

* Use Flask `jsonify` to convert your API data into a valid JSON response object.
