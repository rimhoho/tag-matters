import os
import sys
import configparser
import datetime
import requests
import operator

from pandas.io.json import json_normalize
from flask import Flask, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///monthly_tag"

# db = SQLAlchemy(app)

# Use CofigParser to safely store the password or key
get_key = configparser.ConfigParser()
get_key.read('key_pair.ini')
Times_key = get_key['Times']['key']

from get_data import *


###################################################################
# HTML Pages
###################################################################


@app.route('/')
def home():
    return render_template("index.html")


###################################################################
# RESTful API
###################################################################


# get current month data first
@app.route('/data/init')
def init():
    today = str(datetime.datetime.now())
    data = get_init_data(today[:4], today[5:7])
    return jsonify(data)

    # for top_tag in tags_with_frequency:
    #     multi_articles = {}
    #     for each in reversed(each_metadata) :
    #         if top_tag[0] in multi_articles:
    #             pass      
    #         else:
    #             if len(each['tags']) != 0 and top_tag[0] in each['tags']:
    #                 db.session.add(
    #                     Metadata(
    #                         Tag = top_tag[0],
    #                         Frequency = str(top_tag[1]),
    #                         Title = each['title'],
    #                         Date = each['pub_date'],
    #                         Url = each['url'],
    #                         Description = each['description'],
    #                         img_URL = each['thm_img']
    #                     )
    #                 )
    #             # db.session.query(Metadata).all() = [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]
    # db.session.commit()

    # return jsonify([x.serialize for x in db.session.query(Metadata).all()])


# @app.route('/data/all')
# def api():
#     errors = []
#     try:
#         metadata = models.Metadata(
#         )
#         db.session.add(metadata)
#         db.session.commit()
#     except:
#         errors.append("Unable to add item to database.")
#     return jsonify(metadata)


if __name__ == "__main__":
    app.run(debug=True)
