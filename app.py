import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
meas = Base.classes.measurement
stat = Base.classes.station

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
        f"/api/v1.0/precipitation</br></h1>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    """Return the JSON representation of your dictionary."""

    results = session.query(meas.date, meas.prcp).all()  

    # Create a dictionary from the row data and append to a list of measurements
    all_ms = []
    for r in results:
        ms_dict = {}
        ms_dict["date"] = r.date
        ms_dict["prcp"] = r.prcp
        all_ms.append(ms_dict)

    return jsonify(all_ms)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query of stations
    results = session.query(stat.station).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def temp():
    """query for the dates and temperature observations from a year from the last data point."""
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Query of tobs
    results = session.query(meas.date, meas.tobs).\
    filter(meas.station == 'USC00519281').\
    filter(meas.date >='2016-08-23').\
    filter(meas.date <='2017-08-23').\
    order_by(meas.date).all()

    # results = session.query(meas.date, meas.tobs).all()
    # print(results)

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    # Query of tobs

    if end != None:
        # FILTER ON START AND END
        results = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
            filter(meas.date >= start).\
            filter(meas.date <= end).\
            all()

    else:
        # I ONLY FILTER ON START
        results = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
            filter(meas.date >=start).\
            all()
        
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)



if __name__ == '__main__':
    app.run(debug=True, port=5000)


