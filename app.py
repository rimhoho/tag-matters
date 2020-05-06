import os
import sys
import configparser
import datetime
import requests
import operator

from pandas.io.json import json_normalize
from flask import Flask, jsonify, render_template, redirect

from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, distinct
from flask_sqlalchemy import SQLAlchemy

from model import TimesTable, GoogleTable, RedditTable

###############
# Flask Setup #
###############

app = Flask(__name__)

############
# Database #
############

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monthly_times_tags.db'
db = SQLAlchemy(app)


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


# Get Times data 
@app.route("/times")
def Times():
    
    # Create session and query all data
    times_combined = db.session.query(TimesTable).all()
    db.session.close()

    times_archive = []
    for times_tag in times_combined:
        each_times = {'tag' : times_tag.tag,
                      'periode' : times_tag.periodeM,
                      'frequency' : times_tag.frequency,
                      'title' : times_tag.title,
                      'date' : times_tag.date,
                      'url' : times_tag.url,
                      'img_URL' : times_tag.img_URL}
        times_archive.append(each_times)
    return jsonify(times_archive)


# Get Google Search data 
@app.route("/google")
def Google():
    
    # Create session and query all data
    google_combined = db.session.query(GoogleTable.trendDate, GoogleTable.startDate, GoogleTable.endDate, GoogleTable.busiest, GoogleTable.trendIndex, TimesTable.tag, TimesTable.periodeM).join(TimesTable, TimesTable.id == GoogleTable.fk_times).group_by(GoogleTable.id).all()
    db.session.close()

    google_archive = []
    for google in google_combined:
        each_google = {'tag':google.tag,
                      'periode':google.periodeM,
                      'trendDate' : google.trendDate,
                      'startDate' : google.startDate,
                      'endDate' : google.endDate,
                      'busiest' : google.busiest,
                      'trendIndex' : google.trendIndex}
        google_archive.append(each_google)
    return jsonify(google_archive)


# Get Reddit data 
@app.route("/reddit")
def Reddit():

    # Create session and query all data
    # reddit_combined = db.session.query(RedditTable.postsCount, RedditTable.vote, TimesTable.tag, TimesTable.periodeM).join(TimesTable, TimesTable.id == RedditTable.fk_times).group_by(RedditTable.id).all()
    reddit_combined = db.session.query(RedditTable).all()
    db.session.close()

    reddit_archive = []
    for reddit in reddit_combined:
        each_reddit = {'tag':reddit.tag,
                      'createdDate':reddit.createdDate,
                      'postsCount' : reddit.postsCount,
                      'vote' : reddit.vote}
        reddit_archive.append(each_reddit)
    return jsonify(reddit_archive)

if __name__ == "__main__":
    app.run(debug=True)


