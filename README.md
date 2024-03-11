# SQLAlchemy Challenge

## Project Description
This project involves analyzing climate data for Hawaii using SQLAlchemy, Flask, and data visualization techniques.

## Project Structure
The project directory `sqlalchemy-challenge` contains the following files and folders:
- `app.py`: Flask application for the project
- `climate_starter.ipynb`: Jupyter notebook with the initial climate analysis
- `resources/`: Folder containing data files
  - `hawaii.sqlite`: SQLite database file
  - `hawaii_measurements.csv`: CSV file with measurements data
  - `hawaii_stations.csv`: CSV file with stations data
- `.gitignore`: File specifying which files to ignore in version control
- `README.md`: This file

## Dependencies
The project requires the following dependencies:
- sqlalchemy
- flask
- matplotlib
- numpy
- pandas

## References
- Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910. [Link to the article](https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml)

## Usage
1. Ensure you have the necessary dependencies installed.
2. To analyze the climate data, run the `climate_starter.ipynb` Jupyter notebook. You can open the notebook in Jupyter or any compatible environment to view the analysis.
3. Run `app.py` to start the Flask application.
4. Explore the climate data using the provided endpoints.

## Code Snippet
```python
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import warnings
