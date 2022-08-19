# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask Dependencies
from flask import Flask, jsonify

# Set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect the database into our classes
Base = automap_base()
# reflect tables
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

import app
app = Flask(__name__)

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")

# define the welcome route
    @app.route("/")
# add the routing information for each of the other routes. For this we'll create a function
# and our return statement will have f-strings as a reference to all of the other routes
    def welcome():
        return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:\n
    /api/v1.0/precipitation\n
    /api/v1.0/stations\n
    /api/v1.0/tobs\n
    /api/v1.0/temp/start/end\n
    ''')

# To create the route, add the following code
    @app.route("/api/v1.0/precipitation")
# create the precipitation() function
    def precipitation():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        precipitation = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= prev_year).all()
        return
# Next, write a query to get the date and precipitation for the previous year. 
#Add this query to your existing code

# return a list of all the stations
@app.route("/api/v1.0/stations")

#start by unraveling our results into a one-dimensional array
# convert that array into a list. Then jsonify the list and return it as JSON
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# return the temperature observations for the previous year
@app.route("/api/v1.0/tobs")

def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    # unravel the results into a one-dimensional array and convert that array into a list
    return jsonify(temps=temps)
    # jsonify the list and return result

# report on the minimum, average, and maximum temperatures
# this route is diff from the previous ones in that we will have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats()
def stats(start=None, end=None):
    # # add a start parameter and an end parameter
    
    # create a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Since we need to determine the starting and ending date, add an if-not statement
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # unravel the results into a one-dimensional array and convert them to a list
        temps = list(np.ravel(results))
        return jsonify(temps)
        # jsonify
    
    # calculate the temperature minimum, average, and maximum with the start and end dates using sel list
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # unravel the results into a one-dimensional array and convert them to a list
    temps = list(np.ravel(results))
    return jsonify(temps)
    # jsonify