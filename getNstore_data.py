import json
import requests
import pandas as pd
import numpy as np
import operator
import time
import praw
import nltk
import configparser

from apiclient import discovery
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pytrends.request import TrendReq
from praw.models import MoreComments
from googleapiclient import discovery
from textblob import TextBlob
from pandas.io.json import json_normalize

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

Youtube_service_name = config['Youtube']['YOUTUBE_API_SERVICE_NAME']
Youtube_API_version = config['Youtube']['YOUTUBE_API_VERSION']
Youtube_developer_key = config['Youtube']['DEVELOPER_KEY']


def get_NYTimes_metadata():

    # To get most frequently used tag in NYTimes
    today = str(datetime.today())
    monthly_archive = {}
    frequent_tags_archive = {}

    for yy in reversed(range(2019, int(today[:4]) + 1)):
        if str(yy) == today[:4]:
            ends = int(today[5:7]) + 1
            start = 1
        else:
            ends = 13
            if '0' in today[5:7]:
                start = int(today[6:7])
            else:
                start = int(today[5:7])
        for mm in reversed(range(start,ends)):
            print('--1--',yy,mm)
            parameters = {'api-key': Times_key}           
            archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ str(yy) +'/'+ str(mm) +'.json'
            archives = requests.get(archived_Url, params=parameters).json()

            monthly_article = []
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
                monthly_article.append(articles)
            if len(str(mm)) == 1:
                mm = '0' + str(mm)
            monthly_archive[str(yy)+'-'+str(mm)] = monthly_article

            tag_arr = []
            for m in monthly_article:
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
                if tag in ['School Shootings and Armed Attacks']:
                    tag = 'School Shootings'
                if tag in ['Shutdowns (Institutional)']:
                    tag = 'Shutdowns'
                if tag in ['New York City', 'NYC','NY)','New York State' ]:
                    tag = 'New York State'
                if tag in ['States (US)', 'United States']:
                    tag = 'United States'
                if 'Russian Interference in 2016' in tag:
                    tag = 'Russian interference in the 2016 United States elections'
                if tag in ['Homosexuality and Bisexuality']:
                    tag = 'Homosexuality'
                if tag in ['Biden, Joseph R Jr', 'Biden']:
                    tag = 'Joe Biden'
                if tag in ['Sanders, Bernard', 'Sanders', 'Bernard', 'Bernie Sanders']:
                    tag = 'Bernie Sanders'
                if tag in ['Pete Buttigieg', 'Buttigieg, Pete (1982- )', 'Buttigieg', 'Pete Buttigieg', 'Pete (1982- )']:
                    tag = 'Pete Buttigieg'
                if tag in ['Blacks', 'Black People']:
                    tag = 'Blacks'
                if 'Coronavirus Aid' in tag:
                    tag = 'Coronavirus Aid Relief and Economic Security Act'
                if 'Quarantine' in tag:
                    tag = 'Quarantines'
                if 'Deaths' in tag:
                    tag = 'Deaths'
                if 'Child' in tag:
                    tag = 'Parenting'
                if 'Trump-Ukraine' in tag:
                    tag = 'Trump-Ukraine'
                if tag in ['Donald Trump', 'Weddings and Engagements', 'Women and Girls', 'New York State', 'Primaries and Caucuses', 'United States Politics and Government', 'Politics and Government', 'Books and Literature', 'Television', 'Movies', 'Real Estate and Housing (Residential)', 'United States', 'United States International Relations' 'Primaries and Caucuses', 'United States Economy', 'Elections']:
                    tag = ''

                if tag is not '':
                    if tag in count_tag:
                        count_tag[tag] += 1
                    else:
                        count_tag[tag] = 1   

            # This variable is what we want to get in NYTimes
            tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:15]
            frequent_tags_archive[str(yy)+'-'+str(mm)] = tags_with_frequency

    return monthly_archive, frequent_tags_archive


################################################
monthly_archive = get_NYTimes_metadata()[0]
frequent_tags_archive = get_NYTimes_metadata()[1]
################################################

def get_youtube_numbers(frequent_tags_archive):
    Session = sessionmaker(bind=engine)
    session = Session()

        # Store numbers of each Youtube's comments into DB
        # viewCount = 0
        # commentsCount = 0
        # likeCount = 0
        # search_tags = youtube_object.search().list(q = tag_frequency[0], part = "id, snippet", order = 'relevance', maxResults = max_results, publishedAfter = "2019-05-01T00:00:00Z").execute() 
        # print('start: ', tag_frequency[0])
        # for item in search_tags.get("items", []):
        #     time.sleep(2)
        #     stats = youtube_object.videos().list(part='statistics, snippet', id=item["id"]["videoId"]).execute()
        #     new_viewCount = int(stats.get("items", [])[0]['statistics']['viewCount'])
        #     new_commentsCount = int(stats.get("items", [])[0]['statistics']['commentsCount'])
        #     new_likeCount =  int(stats.get("items", [])[0]['statistics']['likeCount'])
        #     viewCount = viewCount + new_viewCount
        #     commentsCount = commentsCount + new_commentsCount
        #     likeCount = likeCount + new_likeCount
        #     try:
        #         insert_Youtube = YoutubeTable(
        #             tag=tag_frequency[0],
        #             viewCount=viewCount,
        #             commentsCount=commentsCount,
        #             likeCount=likeCount
        #         )
        #         session.add(insert_Youtube)

        #     except Exception as e:
        #         print(" = Unable insert_Youtube to DB : ", tag_frequency[0], " =")
        #         pass
    
    session.commit()

    return

def store_metadata(monthly_archive, frequent_tags_archive):
    today = str(datetime.today())

    # To store tag and other data into the DB connecting Session
    Session = sessionmaker(bind=engine)
    session = Session()
    reddit_metadata = []

    # Connect with Pytrend(Google Search Trend), to get Search Interest Index
    pytrends = TrendReq(hl='en-US', tz=360)

    # Pytrend and PRAW use "frequent_tags_archive" in order to get each demand data
    
    for periode in frequent_tags_archive:
        multi_articles = {}
        for top_tag in frequent_tags_archive[periode]:
            
            # Get specific NYTimes article information per each tags
            for whole_month in list(monthly_archive.values()):
                for each in reversed(whole_month):
                    if top_tag[0] in multi_articles and periode in multi_articles :
                        pass      
                    else:
                        if len(each['tags']) != 0 and top_tag[0] in each['tags']:
                            try:
                                insert_TimesTag = TimesTable(
                                    tag=top_tag[0],
                                    periodeM=periode,
                                    frequency=top_tag[1],
                                    title=each['title'],
                                    date=each['pub_date'],
                                    url=each['url'],
                                    img_URL=each['thm_img'])

                                multi_articles[top_tag[0]] = ''
                                multi_articles[periode] = ''

                                session.add(insert_TimesTag)
                                # session.commit() 
                            except Exception as e:
                                print(" = Unable insert_TimesTag to DB : ", top_tag[0], periode, " =")
                                pass


    frequent_tag_only = {}
    
    for time_period in frequent_tags_archive:
        tag_only = []
        for each in frequent_tags_archive[time_period]:    
            tag_only.append(each[0])
            frequent_tag_only[time_period] = tag_only
            
    for period in frequent_tag_only:
        reddit_posts = {}
        add_post_arr = []

        for top_tag in frequent_tag_only[period]:

            tag_arr = []
            tag_arr.append(top_tag)
            interest_over_time = {}
            
            try:
                pytrends.build_payload(tag_arr, cat=0, timeframe = '2019-05-01 '+ today[:10], geo='', gprop='')
                df = pytrends.interest_over_time().reset_index()
            except Exception as e:
                print(" = Unable search Google Trends : ", top_tag, periode, " =")
                pass
            
            try:
                fk_id = session.query(TimesTable).filter_by(tag=top_tag, periodeM=period).first().id

                for i, frequency in enumerate(df[top_tag]):
                    if frequency == 100:
                        busiest_date = df['date'].iloc[i].strftime("%Y-%m-%d")

                insert_Google = GoogleTable(
                        trendDate = [date.strftime("%Y-%m-%d") for date in df['date']],
                        busiest = busiest_date,
                        trendIndex = [rate for rate in df[top_tag]],
                        fk_times = fk_id)

                session.add(insert_Google)

            except Exception as e:
                print(" = Unable insert_Google to DB : ", top_tag, periode, " =")
                pass
    
    
    reddit = praw.Reddit(client_id = Reddit_client_id,
                         client_secret = Reddit_client_secret,
                         username = Reddit_username,
                         password = Reddit_password,
                         user_agent = Reddit_user_agent)

    # Get top prequently used tag among whole timeframe
    unique_top_tag_only={}
    for periode in frequent_tags_archive:
        for tag_with_F in frequent_tags_archive[periode]:
            if tag_with_F[0] in unique_top_tag_only:
                unique_top_tag_only[tag_with_F[0]] = tag_with_F[1] + unique_top_tag_only[tag_with_F[0]]
            else:
                unique_top_tag_only[tag_with_F[0]] = tag_with_F[1]

    unique_top_tag_only = sorted(unique_top_tag_only.items(),key=operator.itemgetter(1),reverse=True)[:20]

    # # creating Youtube Resource Object 
    # youtube_object = discovery.build(Youtube_service_name, Youtube_API_version, developerKey = Youtube_developer_key)
    
    max_results = 30

    for tag_frequency in unique_top_tag_only:
        
        # Store numbers of each Reddit's comments into DB
        try:
            print('Check tag existing: ', tag_frequency[0])
            subreddit = reddit.subreddit('all')
            time.sleep(2)
            for post in subreddit.search(tag_frequency[0], sort='relevance', syntax='lucene', limit=max_results):
                count = 0;
                if not post.stickied:
                    each_tag_comments = post.comments.list()
                    comments_arr = []
                    for comment in each_tag_comments:
                        if isinstance(comment, MoreComments):
                            continue
                        comments_arr.append(comment.body)
                        count = count + len(comments_arr)

                    try:
                        # fk_id = session.query(TimesTable).filter_by(tag=tag, createdDate=createdAt).first().id
                        insert_Reddit = RedditTable(
                            tag=tag_frequency[0],
                            commentsCount=count
                        )
                        session.add(insert_Reddit)

                    except Exception as e:
                        print(" = Unable insert_Reddit to DB : ", tag_frequency[0], " =")
                        pass
        except Exception as e:
            print(" = Unable search Reddit : ", tag_frequency[0], " =")
            pass
        

    session.commit() 


    return        
                     


store_metadata(monthly_archive, frequent_tags_archive)
