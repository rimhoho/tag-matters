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
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# print('APP_SETTINGS: ', os.environ['APP_SETTINGS'], 'DATABASE_URL: ', db)

# Use CofigParser to safely store the password or key
get_key = configparser.ConfigParser()
get_key.read('key_pair.ini')
Times_key = get_key['Times']['key']

import models
import get_data

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/init')
def init():
    results = {}
    errors = []
    try:
        today = str(datetime.datetime.now())
        parameters = {'api-key': Times_key}    
        archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ today[:4] +'/'+ today[5:7] +'.json'
        archives = requests.get(archived_Url, params=parameters).json()

        each_metadata = []
        for a in archives['response']['docs']:
            articles = {}
            metadata = {}
            metadata['title'] = a['headline']['main']
            metadata['pub_date'] = a['pub_date'][:10]
            metadata['url'] = a['web_url']
            metadata['description'] = a['lead_paragraph']
            if len(a['multimedia']) !=0 and a['multimedia'][0]['url']:
                metadata['thm_img'] = 'https://static01.nyt.com/' + a['multimedia'][0]['url']
            else:
                metadata['thm_img'] = 'no_image_found'
            metadata['tags'] = [''.join(tag['value']) for tag in a['keywords']]
            each_metadata.append(metadata)
            
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
        
        data = []
        for top_tag in tags_with_frequency:
            multi_articles = {}
            for metadata in reversed(each_metadata) :
                if top_tag[0] in multi_articles:
                    pass      
                else:
                    if len(metadata['tags']) != 0 and top_tag[0] in metadata['tags']:
                        multi_articles['Tag'] = top_tag[0]
                        multi_articles['Frequency'] = str(top_tag[1])
                        multi_articles['title'] = metadata['title']
                        multi_articles['pub_date'] = metadata['pub_date']
                        multi_articles['url'] = metadata['url']
                        multi_articles['description'] = metadata['description']
                        multi_articles['thm_img'] = metadata['thm_img']
                        data.append(multi_articles)
        # data = [{'Tag': '', 'Frequency': '', 'Title': '', 'Date': '', 'Url': '', 'Description': '', 'img_URL': ''},{...}]
        print('*' * 20, data)

        for each in data:
            db.session.add_all(models.Metadata(
                Tag = each['Tag'],
                Frequency = each['Frequency'],
                Title = each['Title'],
                Date = each['Date'],
                Url = each['Url'],
                Description = each['Description'],
                img_URL = each['img_URL']))
        db.session.commit()
    except:
        print("Unable to get Data. Please make sure it's valid and try again.")
    return jsonify(data)


# @app.route('/metadata')
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


# @app.route('/popular')
# def reddit():
#     return jsonify()


@app.route('/reddit')
def reddit():
    return jsonify()

if __name__ == "__main__":
    app.run(debug=True)
