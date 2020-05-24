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

from model import TimesTable, GoogleTable, YoutubeTable, MonthlyTagTable, TagByPeriodeTable, UniqueTagNFrequencyTable

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
    google_combined = db.session.query(GoogleTable.trendDate, GoogleTable.busiest, GoogleTable.trendIndex, TimesTable.tag, TimesTable.periodeM).join(TimesTable, TimesTable.id == GoogleTable.fk_times).group_by(GoogleTable.id).all()
    db.session.close()

    google_archive = []
    for google in google_combined:
        each_google = {'tag':google.tag,
                      'periode':google.periodeM,
                      'trendDate' : google.trendDate,
                      'busiest' : google.busiest,
                      'trendIndex' : google.trendIndex}
        google_archive.append(each_google)
    return jsonify(google_archive)

# # Get Reddit data 
# @app.route("/reddit")
# def Reddit():

#     # Create session and query all data
#     reddit_combined = db.session.query(RedditTable).all()
#     db.session.close()

#     reddit_archive = []
#     for reddit in reddit_combined:
#         each_reddit = {'tag':reddit.tag,
#                       'commentCount':reddit.commentCount}
#         reddit_archive.append(each_reddit)
#     return jsonify(reddit_archive)


# Get Youtube data 
@app.route("/youtube")
def Youtube():

    # Create session and query all data
    youtube_combined = db.session.query(YoutubeTable).all()
    db.session.close()

    youtube_archive = []
    for youtube in youtube_combined:
        each_youtube = {'tag':youtube.tag,
                        'viewCount': youtube.viewCount,
                        'commentCount':youtube.commentCount,
                        'likeCount': youtube.likeCount}
        youtube_archive.append(each_youtube)
    return jsonify(youtube_archive)

# Get rest of data 
@app.route("/tagbyperiode")
def rest():
    rest_data_combined = db.session.query(TagByPeriodeTable).all()
    db.session.close()

    rest_data_archive = []
    for rest_data in rest_data_combined:
        each_rest_data = {'periode': rest_data.periodeM,
                          'tags_only': rest_data.tagArr_per_month,
                        #   'article_archives': rest_data.article_archives
                          }
        rest_data_archive.append(each_rest_data)
    return jsonify(rest_data_archive)

@app.route("/frequency")
def frequency():
    unique_tag_frequency_combined = db.session.query(UniqueTagNFrequencyTable).all()
    
    db.session.close()

    unique_tag_frequency_archive = []
    for unique_tag_frequency in unique_tag_frequency_combined:
        each_unique_tag_frequency = {'tag_only': unique_tag_frequency.tag,
                          'frequency': unique_tag_frequency.frequency}
        unique_tag_frequency_archive.append(each_unique_tag_frequency)
    return jsonify(unique_tag_frequency_archive)

@app.route("/month")
def month():
    month_combined = db.session.query(MonthlyTagTable).all()
    db.session.close()

    month_archive = []
    for month in month_combined:
        each_month = {'periode': month.periodeM,
                          'article_archives': month.article_archives}
        month_archive.append(each_month)
    return jsonify(month_archive)

if __name__ == "__main__":
    app.run(debug=True)


