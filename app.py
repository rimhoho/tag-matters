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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///monthly_tag"

db = SQLAlchemy(app)

# Use CofigParser to safely store the password or key
get_key = configparser.ConfigParser()
get_key.read('key_pair.ini')
Times_key = get_key['Times']['key']

from model import *


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
    results = {}
 
    today = str(datetime.datetime.now())
    parameters = {'api-key': Times_key}    
    archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ today[:4] +'/'+ today[5:7] +'.json'
    archives = requests.get(archived_Url, params=parameters).json()

    each_metadata = []
    for a in archives['response']['docs']:
        articles = {}
        articles['title'] = a['headline']['main']
        articles['pub_date'] = a['pub_date'][:10]
        articles['url'] = a['web_url']
        articles['description'] = a['lead_paragraph']
        if len(a['multimedia']) !=0 and a['multimedia'][0]['url']:
            articles['thm_img'] = 'https://static01.nyt.com/' + a['multimedia'][0]['url']
        else:
            articles['thm_img'] = 'no_image_found'
        articles['tags'] = [''.join(tag['value']) for tag in a['keywords']]
        each_metadata.append(articles)
        
    tag_arr = []
    for each in each_metadata:
        for t in each['tags']:
            for string in t.split(', '):
                tag_arr.append(', '.join(string.split(', ')))
                    
    count_tag = {}
    for tag in tag_arr:
        if tag in ['Trump', 'Donald J']:
            tag = 'Donald Trump'
        if tag in ['Joseph R Jr', 'Biden']:
            tag = 'Joe Biden'
        if tag in ['Brett M', 'Supreme Court (US)', 'Kavanaugh']:
            tag = 'Brett Kavanaugh'
        if tag in ['Putin', 'Vladimir V']:
            tag = 'Putin'
        if tag in ['New York City', 'NYC','NY)', 'NY']:
            tag = 'New York City'
            
        if tag in count_tag:
            count_tag[tag] += 1
        else:
            count_tag[tag] = 1   
            
    tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:20]      
    
    for top_tag in tags_with_frequency:
        multi_articles = {}
        for each in reversed(each_metadata) :
            if top_tag[0] in multi_articles:
                pass      
            else:
                if len(each['tags']) != 0 and top_tag[0] in each['tags']:
                    db.session.add(
                        Metadata(
                            Tag = top_tag[0],
                            Frequency = str(top_tag[1]),
                            Title = each['title'],
                            Date = each['pub_date'],
                            Url = each['url'],
                            Description = each['description'],
                            img_URL = each['thm_img']
                        )
                    )
                # db.session.query(Metadata).all() = [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]
    db.session.commit()

    return jsonify([x.serialize for x in db.session.query(Metadata).all()])


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
