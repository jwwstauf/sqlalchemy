import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    rain_totals = []
    for result in results:
        row = {}
        row[result[0]] = result[1]
        rain_totals.append(row)

    return jsonify(rain_totals)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    t_results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2016-08-23', measurement.station == 'USC00519281').all()

    session.close()
    
    temperature_totals = []
    for result in t_results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = result[1]
        temperature_totals.append(row)

    # Create a dictionary from the row data and append to a list of all_passengers

    return jsonify(temperature_totals)   

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    session = Session(engine)
    start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= date).all()
    start_results = []
    for result in start:
        row = {}
        row["min"] = result[0]
        row["avg"] = result[1]
        row["max"] = result[2]
        start_results.append(row)
    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    session = Session(engine)
    start_end = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()
    start_end_results = []
    for result in start_end:
        row = {}
        row["min"] = result[0]
        row["avg"] = result[1]
        row["max"] = result[2]
        start_end_results.append(row)
    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)

