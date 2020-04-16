
import requests
import pandas as pd
import numpy as np
import datetime
import operator
import time
import praw
import nltk
import configparser
import pprint

from pytrends.request import TrendReq
from praw.models import MoreComments
from googleapiclient import discovery
from textblob import TextBlob

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

from model import *


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


# Archive API
def get_times_metadata():
    today = str(datetime.datetime.now())
    monthly_archive = {}
    monthly_popular_tags = {}
    for yy in range(2018, int(today[:4]) + 1):
        if str(yy) == today[:4]:
            ends = int(today[5:7]) + 1
        else:
            ends = 13
        for mm in range(1,ends):
            print(yy,mm)
            parameters = {'api-key': Times_key}           
            archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ str(yy) +'/'+ str(mm) +'.json'
            archives = requests.get(archived_Url, params=parameters).json()

            each_metadata = []
            for a in archives['response']['docs']:
                articles = {}
                articles['title'] = a['headline']['main']
                articles['pub_date'] = a['pub_date'][:10]
                articles['url'] = a['web_url']
                if len(a['multimedia']) !=0 and a['multimedia'][0]['url']:
                    articles['thm_img'] = 'https://static01.nyt.com/' + a['multimedia'][0]['url']
                else:
                    articles['thm_img'] = 'no_image_found'
                articles['tags'] = [''.join(tag['value']) for tag in a['keywords']]
                each_metadata.append(articles)

            tag_arr = []
            for m in each_metadata:
                for t in m['tags']:
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
                if tag in ['Fla', 'Parkland']:
                    tag = 'Parkland'
                if tag in ['Coronavirus Aid', 'Relief', 'and Economic Security Act (2020)']:
                    tag = 'Coronavirus Aid, Relief, and Economic Security Act (2020)'
                if 'Trump-Ukraine' in tag:
                    tag = 'Trump-Ukraine'
                if tag in ['School Shootings and Armed Attacks']:
                    tag = 'School Shootings'
                if tag in ['Shutdowns (Institutional)']:
                    tag = 'Shutdowns'
                if tag in ['New York City', 'NYC','NY)', 'States (US)', 'New York State', 'United States Economy', 'New York Times', 'United States International Relations', 'Appointments and Executive Changes', 'United States', 'Food', 'United States Politics and Government', 'Democratic Party', 'Senate', 'Olympic Games', 'Actors and Actresses', 'Dancing', 'Crossword Puzzles', 'Deaths (Fatalities)', 'World Economic Forum', 'Republican Party', 'Republican Party', 'House of Representatives', 'Politics and Government', 'Research', 'Museums', 'Law and Legislation', 'Justice Department', 'Children and Childhood', 'Photography', 'Pop and Rock Music', 'Restaurants', 'Education (K-12)', 'Corruption (Institutional)', 'Travel and Vacations', 'NY', 'News and News Media', 'Labor and Jobs', 'Suits and Litigation (Civil)', 'Books and Literature', 'Black People', 'Social Media', 'Movies', 'Music', 'Television', 'Cooking and Cookbooks', 'Fashion and Apparel', 'Art', 'Computers and the Internet', 'Theater', 'International Trade and World Market', 'Real Estate and Housing (Residential)', 'New Jersey', 'Colleges and Universities', 'Women and Girls', 'Weddings and Engagements', 'Immigration and Emigration', 'Blacks', 'Deaths (Obituaries)', 'Primaries and Caucuses']:
                    tag = ''

                if tag is not '':
                    if tag in count_tag:
                        count_tag[tag] += 1
                    else:
                        count_tag[tag] = 1   

            tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:40]
                       
            data = []
            for top_tag in tags_with_frequency:
                multi_articles = {}
                for each in reversed(each_metadata) :
                    if top_tag[0] in multi_articles.values():
                        pass      
                    else:
                        if len(each['tags']) != 0 and top_tag[0] in each['tags']:
                            # store the data into variable 'monthly_archive'
                            if len(str(mm)) == 1:
                                mm = '0' + str(mm)
                            multi_articles['Category'] = str(yy) + '-' +  str(mm)
                            multi_articles['Tag'] = top_tag[0]    
                            multi_articles['Frequency'] = str(top_tag[1])
                            multi_articles['Title'] = each['title']
                            multi_articles['Date'] = each['pub_date']
                            multi_articles['Url'] = each['url']
                            multi_articles['img_URL'] = each['thm_img']
                            data.append(multi_articles)
            monthly_archive[str(yy)+'-'+str(mm)] = data
            print('Length: ', len(monthly_archive[str(yy)+'-'+str(mm)]))
#     print('tags_with_frequency', tags_with_frequency)       
    return monthly_archive

# Get a unique tag collection for the search query
def get_trends_Tags(times_metadata):    
    result = {}
    for time_category in times_metadata:
        data = []
        for each in times_metadata[time_category]:     
            data.append(each['Tag'])
            result[time_category] = data
        
    pytrends = TrendReq(hl='en-US', tz=360)
    monthly_interests = {}
    
    for i, Category in enumerate(result):
        print(Category + ': ', len(result[Category]))
        print(result[Category])
        data = []
        for tag in result[Category]:
            if tag in ['Russian Interference in 2016 US Elections and Ties to Trump Associates']:
                tag = 'Russian Ties to Trump'
            if tag in ['Appointments and Executive Changes']:
                tag = 'Appointments and Executive'
            tag_arr = []
            tag_arr.append(tag)
            print(tag)
            interest_over_time = {}
            
            time.sleep(2)
            try:
                pytrends.build_payload(tag_arr, cat=0, timeframe='2018-01-01 ' + str(datetime.datetime.now())[:10], geo='', gprop='')
                time.sleep(2)
                df = pytrends.interest_over_time().reset_index()
                interest_over_time['Tag'] = tag
            

                for i in range(len(list(df[tag]))):
                    try:
                        interest_over_time['Category'] = Category
                        interest_over_time['Date_' + str(i)] = list(df['date'].dt.strftime('%Y-%m-%d'))[i]
                        interest_over_time['Rate_' + str(i)] = list(df[tag])[i]
                    except Exception as e:
                        print('No-result: ', tag)
                        interest_over_time['Date_' + str(i)] = 'None'
                        interest_over_time['Rate_' + str(i)] = 0
                        pass
                    if list(df[tag])[i] == 100:
                        interest_over_time['Busiest_date'] = list(df['date'].dt.strftime('%Y-%m-%d'))[i]
                data.append(interest_over_time)
            except Exception as e:
                print('No-result: ', tag)
                pass
            monthly_interests[Category] = data
    return monthly_interests

def store_metadata():
    times_metadata = get_times_metadata()
    monthly_interests = get_trends_Tags(times_metadata)

    Session = sessionmaker(bind=engine)
    session = Session()

    for time_category in times_metadata:
        for each_metadata in times_metadata[time_category]:
            metadata_row = Times(**each_metadata)
            session.add(metadata_row)

    for time_category in monthly_interests:
        for monthly_tags in monthly_interests[time_category]:
            interest_row = Google(**monthly_tags)
            session.add(interest_row)

    session.commit()

store_metadata()

# Reddit API
def get_reddit_comments(times_metadata):
    reddit = praw.Reddit(client_id = Reddit_client_id,
                         client_secret = Reddit_client_secret,
                         username = Reddit_username,
                         password = Reddit_password,
                         user_agent = Reddit_user_agent)

    tags = {}
    for time_category in times_metadata:
        data = []
        for each in times_metadata[time_category]:     
            data.append(each['Tag'])
            tags[time_category] = data

    reddit_metadata = []
    for tag in tags:
#         if tag in ['OlympicGames', 'Shooting', 'NewYorkCity', 'InternationalTradeandWorldMarket', 'Impeachment', 'MidtermElections', 'Elections', 'Senate', 'Parkland', 'GovernmentShutdowns', 'BrettKavanaugh', 'UnitedStatesPoliticsandGovernment', 'PresidentialElectionof2020', 'PoliticsandGovernment', 'ChristineBlasey', 'WomenandGirls', 'Sanders', 'Immigration', 'Iran']:
#             pass
#         else:
        print(tag)
        subreddit = reddit.subreddit('all')
        each_tag = {}
        for post in subreddit.search(tag, limit=5):
            each_tag['Tag'] = tag
            each_tag['Title'] = post.title
            each_tag['Url'] = post.url
            each_tag_comments = post.comments.list()
            comments_arr = []
            for comment in each_tag_comments:
                if isinstance(comment, MoreComments):
                    continue
                comments_arr.append(comment.body)
            each_tag['Comments'] = comments_arr
        reddit_metadata.append(each_tag)
    return reddit_metadata



    