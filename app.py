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

from model import TimesTable, GoogleBTable, GoogleDTable, GoogleITable, YoutubeTable

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
    google_combined = db.session.query(GoogleDTable.trendDate, GoogleBTable.busiest, GoogleITable.trendIndex, TimesTable.tag, TimesTable.periodeM).join(TimesTable, TimesTable.id == GoogleTable.fk_times).group_by(GoogleTable.id).all()
    db.session.close()

    google_archive = []
    for google in google_combined:
        each_google = {'tag':google.tag,
                      'periode':google.periodeM,
                      'trendDate' : google.trendDate,
                      'busiest' : google.busiest,
                      'trendIndex' : google.trendIndex}
        google_archive.append(each_google)

    print('####', google_archive[0])
    print('****', jsonify(google_archive))
    return jsonify(google_archive)

# Get Youtube data 
@app.route("/youtube")
def Youtube():
    # Create session and query all data
    youtube_combined = db.session.query(YoutubeTable).all()
    db.session.close()

    youtube_archive = []
    for youtube in youtube_combined:
        each_youtube = {'tag':youtube.tag,
                        'url':youtube.url,
                        'title':youtube.title,
                        'img_url':youtube.img_url,
                        'viewCount': youtube.viewCount,
                        'commentCount':youtube.commentCount,
                        'likeCount': youtube.likeCount}
        youtube_archive.append(each_youtube)
    return jsonify(youtube_archive)

# # Get rest of data 
# @app.route("/tagByperiode")
# def rest():
#     top_tags_combined = db.session.query(TagByPeriodeTable).all()
#     db.session.close()

#     monthly_top_tags = []
#     for top_tags in top_tags_combined:
#         each_top_tags = {'periode': top_tags.periodeM,
#                          'top_tag': top_tags.tagArr_per_month
#                           }
#         monthly_top_tags.append(each_top_tags)
#     return jsonify(monthly_top_tags)

if __name__ == "__main__":
    app.run(debug=True)
