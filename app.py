#  import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)
# save the reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#  Create an app, being sure to pass __name__
app = Flask(__name__)

#  Define what to do when a user hits the /about route

# List all routes that are available.
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"<h2>Climate Exploration for Hawaii</h2>"
        f"<p><i>From 2010-01-01</i> to <i>2017-08-23</i></p>"
        f"<img src='https://cdn.travelpulse.com/images/54aaedf4-a957-df11-b491-006073e71405/ee952e9e-f09c-49c2-bc5d-4303c880173a/630x355.jpg'\ width='350'>"    
        f"<h3>Available Routes:</h3>"
        f"<ul><li>/api/v1.0/precipitation</li>"
        f"<li>/api/v1.0/stations</li>"
        f"<li>/api/v1.0/tobs</li>"
        f"<li>/api/v1.0/start_date</li>"
        f"<li>/api/v1.0/start_date/end_date</li></ul>"
        f"<h3>Documentation</h3>"
        f"<dl><dl><i>precipitation</i></dl><dd>-  a dictonary using date as the key and precipitation as the value.</dd>"
        f"<dl><dl><i>stations</i></dl><dd>-  a list of station names.</dd>"
        f"<dl><dl><i>tobs</i></dl><dd>-  a list of temperature observations (TOBS) for the previous year (the most active station).</dd>"
        f"<dl><dl><i>start_date</i></dl><dd>- minimum temperature(TMIN), the average temperature(TAVG), and the max temperature(TMAX) for all\
        dates greater than and equal to the 'start_date'(date format like 2000-01-01).</dd>"
        f"<dl><dl><i>start_date/end_date</i></dl><dd>- minimum temperature(TMIN), the average temperature(TAVG), and the max temperature(TMAX) for all dates between the 'start_date' and 'end_date' inclusive (date format like 2000-01-01).</dd>"        
    )
#  Define what to do when a user hits the index route

#Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    session.close()
    return jsonify(dict(results))

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    result =list(np.ravel(results))
    return jsonify(result)
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tob_ls_t = session.query(Measurement.tobs).\
    filter(Measurement.date>='2016-08-23').\
    filter(Measurement.station =='USC00519281').all()
    session.close()
    result =list(np.ravel(tob_ls_t))
    return jsonify(result)
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def s(start):
    session = Session(engine)
    tob_ls_t = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date>=start).all()
    session.close()
    result =list(np.ravel(tob_ls_t))
    result_dict = {'TMIN':result[0],'TAVG':round(result[1],1),'TMAX ':result[2]}
    return jsonify(result_dict)
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def s_e(start,end):
    session = Session(engine)
    tob_ls_t = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()
    result =list(np.ravel(tob_ls_t))
    result_dict = {'TMIN':result[0],'TAVG':round(result[1],1),'TMAX ':result[2]}
    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)