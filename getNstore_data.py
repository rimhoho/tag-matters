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

Youtube_YOUTUBE_API_SERVICE_NAME = config['Youtube']['YOUTUBE_API_SERVICE_NAME']
Youtube_YOUTUBE_API_VERSION = config['Youtube']['YOUTUBE_API_VERSION']
Youtube_DEVELOPER_KEY = config['Youtube']['DEVELOPER_KEY']


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
                                print(e)#, " = Unable to insert_TimesTag to database.")
                                pass

    # Connect with PRAW(Reddit), to get numbers of the post and voteup
    reddit = praw.Reddit(client_id = Reddit_client_id,
                            client_secret = Reddit_client_secret,
                            username = Reddit_username,
                            password = Reddit_password,
                            user_agent = Reddit_user_agent)

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

            # Get spicific timeframe for filltering the Google Search Trends results per each tag by period
            datetyped_period = datetime.strptime(period, "%Y-%m")
            one_month_ago = (datetyped_period + relativedelta(months=-1)).replace(day=datetime.today().day).strftime("%Y-%m-%d")
            if period == today[:7]:
                one_month_later = today[:10]
            else:
                one_month_later = (datetyped_period + relativedelta(months=+1)).replace(day=datetime.today().day).strftime("%Y-%m-%d")
            
            time.sleep(2)

            # Call pytrends by tag_arr and store them into dataframe
            try:
                pytrends.build_payload(tag_arr, cat=0, timeframe = one_month_ago + ' ' + one_month_later, geo='', gprop='')
                df = pytrends.interest_over_time().reset_index()
            except Exception as e:
                print(e, " = Unable to search on Google Trends by ", tag_arr)
                pass
            
            try:
                fk_id = session.query(TimesTable).filter_by(tag=top_tag, periodeM=period).first().id

                for i, frequency in enumerate(df[top_tag]):
                    if frequency == 100:
                        busiest_date = df['date'].iloc[i].strftime("%Y-%m-%d")

                insert_Google = GoogleTable(
                        trendDate = [date.strftime("%Y-%m-%d") for date in df['date']],
                        startDate = one_month_ago,
                        endDate = one_month_later,
                        busiest = busiest_date,
                        trendIndex = [rate for rate in df[top_tag]],
                        fk_times = fk_id)

                session.add(insert_Google)

            except Exception as e:
                print(e, " = Unable to insert_Google to database.")
                pass
            

            # Cleaning tags is mandatory to get accurate results on the Reddit's Post
            if top_tag in ['Biden, Joseph R Jr']:
                top_tag = 'Joe Biden'
            if top_tag in ['Sanders, Bernard']:
                top_tag = 'Bernie Sanders'
            if top_tag in ['Coronavirus (2019-nCoV)']:
                top_tag = 'Coronavirus'
            reddit_comments = []
            subreddit = reddit.subreddit('all')
            time.sleep(2)

            for post in subreddit.search(top_tag, sort='relevance', syntax='lucene', time_filter='month', limit=100):
                if not post.stickied:
                    # if today[]
                    # CreatedAt = datetime.fromtimestamp(post.created_utc).isoformat()[:10]
                    each_tag = {}
                    each_tag['Tag'] = top_tag
                    each_tag['Title'] = post.title
                    each_tag['CreatedAt'] = datetime.fromtimestamp(post.created_utc).isoformat()[:10]
                    each_tag['DiscussionAbout'] = post.url
                    each_tag['Ups'] = post.ups
                    add_post_arr.append(each_tag)

            reddit_posts[period] = add_post_arr
        reddit_metadata.append(reddit_posts)

    # To get numbers of each Reddit's posts/voteUp/voteDown per month
    add_tag = {}
    for item in reddit_metadata:    
        for period in item: 
            monthly_posts = []
           
            for each_post in item[period]:
                each_post['CreatedAt'] = each_post['CreatedAt'][:7]

                if each_post['Tag'] not in add_tag:
                    byTime = {}
                    add_tag[each_post['Tag']] = byTime
                    if each_post['CreatedAt'] in byTime:
                        byTime[each_post['CreatedAt']][0] += 1
                        byTime[each_post['CreatedAt']][1] += each_post['Ups']
                    else:
                        add_freq_votes = []
                        byTime[each_post['CreatedAt']] = add_freq_votes
                        add_freq_votes.append(1)
                        add_freq_votes.append(each_post['Ups'])
                else:
                    if each_post['CreatedAt'] in byTime:
                        byTime[each_post['CreatedAt']][0] += 1
                        byTime[each_post['CreatedAt']][1] += each_post['Ups']
                    else:
                        add_freq_votes = []
                        byTime[each_post['CreatedAt']] = add_freq_votes
                        add_freq_votes.append(1)
                        add_freq_votes.append(each_post['Ups'])
                        
            monthly_posts.append(add_tag)
    
    # Store numbers of each Reddit's posts/voteUp into DB
    for each_tag_with_prd in monthly_posts:
        for tag in each_tag_with_prd:
            for createdAt in each_tag_with_prd[tag]:
                try:
                    # fk_id = session.query(TimesTable).filter_by(tag=tag, createdDate=createdAt).first().id

                    insert_Reddit = RedditTable(
                        tag=tag,
                        createdDate=createdAt,
                        postsCount=each_tag_with_prd[tag][createdAt][0],
                        vote=each_tag_with_prd[tag][createdAt][1])

                    session.add(insert_Reddit)

                except Exception as e:
                    print(e, " = Unable to insert_Reddit to database.")
                    pass
                        
    session.commit()                  


store_metadata(monthly_archive, frequent_tags_archive)
