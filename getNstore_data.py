import json
import requests
import pandas as pd
import numpy as np
import operator
import time
import praw
import nltk
import configparser
import re

from apiclient import discovery
from datetime import datetime, date, timedelta
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


######################################################################################
# Create 4 functions to get data for fetching data : Initial New York Times metadata #
######################################################################################

def cleaning_tag(tag):  
    if tag in ['School Shootings and Armed Attacks']:
        tag = 'School Shootings'
    if tag in ['Midland-Odessa, Tex, Shooting (2019)', 'Dayton, Ohio, Shooting (2019)', 'El Paso, Tex, Shooting (2019)', 'El Paso', 'Dayton', 'Shooting (2019)', 'Tex']:
        tag = 'Shootings'
    if tag in ['Homosexuality and Bisexuality']:
        tag = 'Homosexuality'
    if tag in ['Biden, Joseph R Jr']:
        tag = 'Joe Biden'
    if tag in ['Floyd George (d 2020)', 'George Floyd Protests (2020)']:
        tag = 'George Floyd Protests (2020)'
    if 'Security Act (2020)' in tag:
        tag = 'Coronavirus Aid Relief and Economic Security Act'
    if 'Suleimani' in tag:
        tag = 'Qasem Soleimani'
    if 'Homicides' in tag:
        tag ='Homicides'
    if 'Buttigieg' in tag:
        tag = 'Pete Buttigieg'
    if 'Police Brutality' in tag:
        tag = 'Police Brutality'
    if 'Trump-Ukraine' in tag:
        tag = 'Trump Ukraine Whistle blower'
    if 'Shutdowns' in tag:
        tag = 'Shutdowns'
    if 'Quarantine' in tag:
        tag = 'Quarantines'
    if 'Deaths' in tag:
        tag = 'Deaths'
    if 'Russian Interference in 2016' in tag:
        tag = 'Russian interference in the 2016 United States elections'
    if 'Syria' in tag:
        tag = 'Syria'    
    if tag in ['Deaths','Social Media', 'Cooking and Cookbooks', 'Computers and the Internet', 'California', 'Iowa', 'Children and Childhood', 'Babies and Infants', 'News and News Media', 'Theater', 'Trump, Donald J', 'Weddings and Engagements', 'Impeachment', 'Senate', 'Discrimination', 'Art', 'Debates (Political)', 'Women and Girls','States (US)', 'United States', 'New York State', 'New York City', 'New York Times', 'NYC', 'NY', 'Primaries and Caucuses', 'United States Politics and Government', 'Politics and Government', 'Democratic Party', 'Republican Party', 'United States Defense and Military Forces', 'Presidential Election of 2020', 'Books and Literature', 'Television', 'Movies', 'Real Estate and Housing (Residential)', 'United States', 'United States International Relations', 'International Trade and World Market',  'House of Representatives', 'Primaries and Caucuses', 'United States Economy', 'Elections']:
        tag = ''
    return tag

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
                start = int(today[6:7]) + 1
            else:
                start = int(today[5:7]) + 1

        for mm in reversed(range(start, ends)):
            print('* * ', yy, mm)
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
                
                cleaning_article = map(cleaning_tag,  [''.join(tag['value']) for tag in a['keywords']])
                articles['tags'] = [changed_tag if ', ' not in changed_tag else changed_tag.replace(", ", " ") for changed_tag in cleaning_article]
                
                monthly_article.append(articles)
                
            if len(str(mm)) == 1:
                mm = '0' + str(mm)
            monthly_archive[str(yy)+'-'+str(mm)] = monthly_article
            
            count_tag = {}
            for m in monthly_article:
                for tag in m['tags']:
                    if tag is not '':
                        if tag in count_tag:
                            count_tag[tag] += 1
                        else:
                            count_tag[tag] = 1   

            # This variable is what we want to get in NYTimes
            tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:10]
            frequent_tags_archive[str(yy)+'-'+str(mm)] = tags_with_frequency

    return monthly_archive, frequent_tags_archive

def call_monthly_top_tags(frequent_tags_archive, number):
    monthly_top_tags = {}
    for time_period in frequent_tags_archive.keys():
        tag_only = []
        for each in frequent_tags_archive[time_period][:number]: 
            tag_only.append(each[0])
            monthly_top_tags[time_period] = tag_only
    return monthly_top_tags

def call_unique_whole_tag_list(monthly_top_tags):
    count_tag = {}
    for periode in monthly_top_tags:
        for tag in monthly_top_tags[periode]:
            if tag is not '' and tag in count_tag:
                count_tag[tag] += 1
            else:
                count_tag[tag] = 1  
    unique_whole_tag_list = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)
    unique_whole_tag_list = [tags_f for tags_f in unique_whole_tag_list]
    return unique_whole_tag_list 

#####################################################
# Create a Class for Fetching 3 different endpoints #
#####################################################

class Fetcher(object):

    def store_times(self, monthly_archive, frequent_tags_archive, session):
        print('* Srart to Store Times');

        multi_articles = {}
        been_used = []
        for periode in frequent_tags_archive:
            for top_tag in frequent_tags_archive[periode]:
                print(periode);
                for each in reversed(monthly_archive[periode]):
                    if top_tag[0] in multi_articles and periode in multi_articles[top_tag[0]]:
                        pass                             
                    else:
                        if len(each['tags']) != 0 and top_tag[0] in each['tags'] and each['title'] not in been_used:
                            try:
                                print(top_tag[0]);
                                insert_TimesTag = TimesTable(
                                    tag=top_tag[0],
                                    periodeM=periode,
                                    frequency=top_tag[1],
                                    title=each['title'],
                                    date=each['pub_date'],
                                    url=each['url'],
                                    img_URL=each['thm_img'])

                                multi_articles[top_tag[0]] = periode
                                been_used.append(each['title'])
                                    
                                session.add(insert_TimesTag)
                                session.flush()
                            except Exception as e:
                                print(" = Unable insert_TimesTag to DB : ", periode, top_tag[0], " =", e)
                                pass   
                     
    def store_google(self, unique_whole_tag_list, session):
        print('* Srart to Call/Store Google');

        today = datetime.today()
        one_year_before = str(today.replace(day=1) - timedelta(days=355))[:10] + ' '
        # Connect with Pytrend(Google Search Trend), to get Search Interest Index
        pytrends = TrendReq(hl='en-US', tz=360)

        for periode in unique_whole_tag_list:
            add_post_arr = []

            for top_tag in unique_whole_tag_list[periode]:
                tag_arr = []
                tag_arr.append(top_tag)
                interest_over_time = {}
                
                try:
                    time.sleep(3)
                    pytrends.build_payload(tag_arr, cat=0, timeframe = one_year_before + str(datetime.today())[:10], geo='', gprop='')
                    time.sleep(3)
                    df = pytrends.interest_over_time().reset_index()
                except Exception as e:
                    print(" = Unable search Google Trends : ", top_tag, periode, " =", e)
                    pass
                
                try:
                    fk_id = session.query(TimesTable).filter_by(tag=top_tag, periodeM=periode).first().id
                    print('= Existing fk_id? =', fk_id)
                    for i, frequency in enumerate(df[top_tag]):
                        if frequency == 100:
                            busiest_date = df['date'].iloc[i].strftime("%Y-%m-%d")

                    insert_Google = GoogleTable(
                            trendDate = [date.strftime("%Y-%m-%d") for date in df['date']],
                            busiest = busiest_date,
                            trendIndex = [rate for rate in df[top_tag]],
                            fk_times = fk_id)

                    session.add(insert_Google)
                    session.flush()
                except Exception as e:
                    print(" = Unable insert_Google to DB : ", periode, top_tag, e, " =")
                    pass

    def call_Youtube(self, unique_whole_tag_list):
        print('* Srart to Call Youtube');

        # creating Youtube Resource Object 
        youtube_object = discovery.build(Youtube_service_name, Youtube_API_version, developerKey = Youtube_developer_key)
        today = datetime.today()
        pre_month = str(today.replace(day=1) - timedelta(days=22))[:10]
        max_results = 4
        youtube_metadata = []
        
        for top_tag in unique_whole_tag_list:
            viewCount = 0
            commentCount = 0
            likeCount = 0
            turned_off_comments = 0
            video = {}
            contain_stats = {}

            time.sleep(10)
            search_tags = youtube_object.search().list(q = top_tag[0], part = "id, snippet", order = 'relevance', maxResults = max_results, publishedAfter = pre_month + "T00:00:00Z").execute() 
            
            for item in search_tags.get("items", []):
                try:
                    url = 'www.youtube.com/watch?v=' + item['id']['videoId']
                    title = item['snippet']['title']
                    if 'medium' in item['snippet']['thumbnails']:
                        img_url = item['snippet']['thumbnails']['medium']
                    else:
                        img_url = item['snippet']['thumbnails']['default']

                    time.sleep(10)
                    stats = youtube_object.videos().list(part='statistics, snippet', id=item["id"]["videoId"]).execute()
                    time.sleep(10)
                    viewCount = int(stats.get("items", [])[0]['statistics']['viewCount'])
                    likeCount =  int(stats.get("items", [])[0]['statistics']['likeCount'])
                    commentCount = int(stats.get("items", [])[0]['statistics']['commentCount'])

                except Exception as e:
                    print(" = Unable search Youtube : ", top_tag[0], " =", e)
                    if e == 'commentCount':
                        new_likeCount = 0 #'Comments are turned off'
                        contain_stats['turned_off_comments'] = 0
                    elif e == 'likeCount':
                        new_likeCount = 0
                    elif e == 'viewCount':
                        new_viewCount = 0

                if 'viewCount' in contain_stats:
                    contain_stats['viewCount'] = contain_stats['viewCount'] + viewCount
                else:
                    contain_stats['viewCount'] = viewCount
                if 'commentCount' in contain_stats:
                    contain_stats['commentCount'] = contain_stats['commentCount'] + commentCount
                else:
                    contain_stats['commentCount'] = commentCount
                if 'likeCount' in contain_stats:
                    contain_stats['likeCount'] = contain_stats['likeCount'] + likeCount
                else:
                    contain_stats['likeCount'] = likeCount
                if 'turned_off_comments' in contain_stats:
                    contain_stats['turned_off_comments'] = contain_stats['turned_off_comments'] + 1
                
                if top_tag[0] in video.keys():
                    pass
                else:
                    video['tag'] = top_tag[0]
                    video['url'] = url
                    video['title'] = title
                    video['img_url'] = img_url
                    video['stats'] = contain_stats       
            youtube_metadata.append(video)   
        return youtube_metadata

    def store_youtube(self, youtube_metadata, session):
        print('* Srart to Store Youtube');

        for each_youtube in youtube_metadata:
            try:
                insert_Youtube = YoutubeTable(
                    tag=each_youtube['tag'],
                    url=each_youtube['url'],
                    title=each_youtube['title'],
                    img_url=each_youtube['img_url'],
                    viewCount=each_youtube['stats']['viewCount'],
                    commentCount=each_youtube['stats']['commentCount'],
                    likeCount=each_youtube['stats']['likeCount']
                )
                session.add(insert_Youtube)
                session.flush()
            except Exception as e:
                print(" = Unable insert_Youtube to DB : ", each_youtube['tag'], " =", e)
                pass

    def store_rest_data(self, monthly_top_tags, session):
        try:

            for periode in monthly_top_tags.keys():
                insert_monthly_top_tags = TagByPeriodeTable(
                    periodeM = periode,
                    tagArr_per_month = monthly_top_tags[periode]
                    )
                session.add(insert_monthly_top_tags)

            for tag_frequency in tags_appeared_every_month:
                insert_tags_appeared_every_month = TagAppearedEveryMonthTable(
                    tag = tag_frequency[0],
                    frequency = tag_frequency[1]
                    )
                session.add(insert_tags_appeared_every_month)

        except Exception as e:
                print(" = Unable insert_rest_data to DB = ", e)
                pass
#############################################################
# Call a function to run all fetch within the same session  # 
#############################################################

def run_all_fetch():
    # To store tag and other data into the DB connecting Session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    monthly_archive = get_NYTimes_metadata()[0]
    frequent_tags_archive = get_NYTimes_metadata()[1]
    monthly_top_tags = call_monthly_top_tags(frequent_tags_archive, 10)
    unique_whole_tag_list = call_unique_whole_tag_list(monthly_top_tags)
    try:
        f1 = Fetcher()
        f1.store_times(monthly_archive, frequent_tags_archive, session)
        f1.store_google(monthly_top_tags, session)

        youtube_metadata = f1.call_Youtube(unique_whole_tag_list)
        print('*'*20)
        print(youtube_metadata)
        print('*'*20)
        f1.store_youtube(youtube_metadata, session)
        f1.store_rest_data(monthly_top_tags, session)    
        session.commit()
    except Exception as e:
        print('= Cannot store into DB, why? =', e)
    finally:
        session.close()


run_all_fetch()