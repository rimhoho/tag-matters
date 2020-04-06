import os
import sys
import configparser
import datetime
import requests
import operator

from pandas.io.json import json_normalize
from flask import Flask, jsonify, render_template, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, distinct
from flask_sqlalchemy import SQLAlchemy


#######################
# Get password or key #
#######################

config = configparser.ConfigParser()
config.read('key_pair.ini')

Times_key = config['Times']['key']

Reddit_client_id = config['Reddit']['client_id']
Reddit_client_secret = config['Reddit']['client_secret']
Reddit_username = config['Reddit']['username']
Reddit_password = config['Reddit']['password']
Reddit_user_agent = config['Reddit']['user_agent']

Youtube_YOUTUBE_API_SERVICE_NAME = config['Youtube']['YOUTUBE_API_SERVICE_NAME']
Youtube_YOUTUBE_API_VERSION = config['Youtube']['YOUTUBE_API_VERSION']
Youtube_DEVELOPER_KEY = config['Youtube']['DEVELOPER_KEY']


###############
# Flask Setup #
###############

app = Flask(__name__)


############
# Database #
############

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monthly_times_tags.db'
db = SQLAlchemy(app)

################
# Define Model #
################


class Metadata(db.Model): 
    __tablename__ = 'times'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(25))
    Tag = db.Column(db.String(255))
    Frequency = db.Column(db.String(255))
    Title = db.Column(db.String(255))
    Date = db.Column(db.String(25))
    Url = db.Column(db.String(255))
    img_URL = db.Column(db.String(255))


##############
# HTML Pages #
##############


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


###############
# RESTful API #
###############


# Get Times Metadata 
@app.route("/metadata")
def TimesData():
    """Return the monthly frequency Times tags""" 
    # Create session and query all data
    results = db.session.query(
        Metadata.Category,
        Metadata.Tag,
        Metadata.Frequency,
        Metadata.Title,
        Metadata.Date,
        Metadata.Url,
        Metadata.img_URL
    ).all()

    db.session.close()

    # Results of the query
    times_metadata = []
    for Category, Tag, Frequency, Title, Date, Url, img_URL in results:
        each_metadata = {}
        each_metadata['Category'] = Category
        each_metadata['Tag'] = Tag
        each_metadata['Frequency'] = Frequency
        each_metadata['Title'] = Title
        each_metadata['Date'] = Date
        each_metadata['Url'] = Url
        each_metadata['img_URL'] = img_URL
        times_metadata.append(each_metadata)

    

    return jsonify(times_metadata)



if __name__ == "__main__":
    app.run(debug=True)
