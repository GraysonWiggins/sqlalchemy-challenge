
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from datetime import datetime, timedelta
import os



# Get the directory of the script
script_dir = os.path.dirname(__file__)
db_filename = "hawaii.sqlite"


# Construct the relative path to the database file
db_path = os.path.join(script_dir, "Resources", db_filename)

# Create the engine using the relative path to the database file
engine = create_engine(f"sqlite:///{db_path}")

# # #################################################
# # # Database Setup
# # #################################################

# # # reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create our session (link) from Python to the DB
session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)

# #################################################
# # Flask Routes
# #################################################
@app.route('/')
def home():
    routes = [
        '/',
        '/api/v1.0/precipitation',
        '/api/v1.0/stations',
        '/api/v1.0/tobs',
        '/api/v1.0/<start>',
        '/api/v1.0/<start>/<end>'
    ]
    return jsonify({"Available Routes": routes})

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Calculate the date one year from the last date in the dataset
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date.replace(year=last_date.year - 1).strftime('%Y-%m-%d')

    # Perform a query to retrieve the data and precipitation scores for the last 12 months without passing the date as a variable
    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_ago
    ).order_by(Measurement.date).all()
    

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
    # Query all stations
    results = session.query(Station.station).all()
    
    # Convert the query results to a list
    station_list = [station for station, in results]
    
    return jsonify({"Stations": station_list})
@app.route('/api/v1.0/tobs')
def tobs():
    # Query the most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]
    
    # Get the most recent date for the most active station
    most_recent_date = session.query(func.max(Measurement.date)).filter(Measurement.station == most_active_station).scalar()
    most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')
    # Calculate the date one year from the last date in the dataset
    one_year_ago = most_recent_date.replace(year=most_recent_date.year - 1)
    
    # Query temperature observations for the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == most_active_station,
        Measurement.date >= one_year_ago
    ).order_by(Measurement.date).all()
    # Convert the query results to a list of dictionaries
    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in results]
    
    return jsonify(tobs_list)
@app.route('/api/v1.0/<start>')
def start_date(start):
    # Query for TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    # Convert the query results to a dictionary
    temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    
    return jsonify(temp_stats)
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Query for TMIN, TAVG, and TMAX for dates between the start and end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    
    # Convert the query results to a dictionary
    temp_stats = {"TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}
    
    return jsonify(temp_stats)
if __name__ == '__main__':
    app.run(debug=True)


