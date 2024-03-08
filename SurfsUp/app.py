# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd

import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/austi/OneDrive/Desktop/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-m-d <br/>"
        f"/api/v1.0/yyyy-m-d/yyyy-m-d"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        """Return a list of all precipitation from the last year"""


        # Query all preciptation
        prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= dt.date(2016,8,23)).all()

        # Convert list of tuples into a callable dictionary
        all_prcp_data = []
        for date, prcp in prcp_data:
              prcp_dict = {}
              prcp_dict["Date"] = date
              prcp_dict["Precipitation"] = prcp
              all_prcp_data.append(prcp_dict)

        return jsonify(all_prcp_data)


@app.route("/api/v1.0/stations")
def station():
        """Return a list of all active stations"""


        # Query all preciptation
        station_data = session.query(stations.station).all()

        # Convert list of tuples into a callable dictionary
        all_stations = list(np.ravel(station_data))

        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
        """Return the dates and temperature observations of the most-active station for the previous year of data."""

        # Query all preciptation
        active_station_temps = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= dt.date(2016,8,23)).all()

        # Convert list of tuples into a callable dictionary
        all_acive_data = []
        for sdate, stemp in active_station_temps:
              active_temp_dict = {}
              active_temp_dict["Date"] = sdate
              active_temp_dict["Temperature"] = stemp
              all_acive_data.append(active_temp_dict)

        return jsonify(all_acive_data)


@app.route("/api/v1.0/<start>")
def temp_data(start):
    """Fetch the min, avg, and max temp whose date matches
       the path variable supplied by the user."""
    
    start_date =  dt.datetime.strptime(start,"%Y-%m-%d")
    
        #Fetch each date's min, max, and average
    temp_measures = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()

    temp_measures_data = []
    for Tdate, TMIN, TMAX, TAVG in temp_measures:
          temp_measures_dict = {}
          temp_measures_dict["Date"] = Tdate
          temp_measures_dict["Min_Temp"] = TMIN
          temp_measures_dict["Max_Temp"] = TMAX
          temp_measures_dict["Avg_Temp"] = TAVG
          temp_measures_data.append(temp_measures_dict)
    
    return jsonify(temp_measures_data)


@app.route("/api/v1.0/<strt>/<end>")
def temp_between(strt,end):
    """Fetch the min, avg, and max temp whose dates match
       the path variables supplied by the user."""
    
    s_date =  dt.datetime.strptime(strt,"%Y-%m-%d")
    e_date =  dt.datetime.strptime(end,"%Y-%m-%d")
    
        #Fetch each date's min, max, and average
    temp_btwn = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter((measurement.date >= s_date)| (measurement.date <= e_date)).all()

    temp_btwn_data = []
    for Bdate, BMIN, BMAX, BAVG in temp_btwn:
          temp_btwn_dict = {}
          temp_btwn_dict["Date"] = Bdate
          temp_btwn_dict["Min_Temp"] = BMIN
          temp_btwn_dict["Max_Temp"] = BMAX
          temp_btwn_dict["Avg_Temp"] = BAVG
          temp_btwn_data.append(temp_btwn_dict)
    
    return jsonify(temp_btwn_data)


#End Session
session.close()

if __name__ == '__main__':
      app.run(debug=True)