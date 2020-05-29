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


######################################################################################
# Create 4 functions to get data for fetching data : Initial New York Times metadata #
######################################################################################

def cleaning_tag(tag):
    if tag in ['Trump', 'Donald J']:
        tag = 'Donald Trump'
    if tag in ['Joseph R Jr', 'Biden']:
        tag = 'Joe Biden'
    if tag in ['Barr, William P', 'Barr', 'William P']:
        tag = 'Barr William P'
    if tag in ['Mueller, Robert S III', 'Mueller', 'Robert S III']:
        tag = 'Mueller Robert S III'
    if tag in ['Sanders, Bernard', 'Sanders', 'Bernard', 'Bernie Sanders']:
        tag = 'Bernie Sanders'
    if tag in ['Pete Buttigieg', 'Buttigieg, Pete (1982- )', 'Buttigieg', 'Pete Buttigieg', 'Pete (1982- )']:
        tag = 'Pete Buttigieg'
    if tag in ['Bloomberg, Michael R', 'Michael R', 'Bloomberg']:
        tag = 'Michael Bloomberg'
    if tag in ['Suleimani, Qassim', 'Suleimani', 'Qassim']:
        tag = 'Soleimani Qassem'
    if tag in ['Warren, Elizabeth', 'Warren', 'Elizabeth']:
        tag = 'Elizabeth Warren'
    if tag in ['Brett M', 'Supreme Court (US)', 'Kavanaugh']:
        tag = 'Brett Kavanaugh'
    if tag in ['Putin', 'Vladimir V']:
        tag = 'Putin'
    if tag in ['Coronavirus Aid', 'Relief', 'and Economic Security Act (2020)']:
        tag = 'Coronavirus Aid, Relief, and Economic Security Act (2020)'
    if tag in ['School Shootings and Armed Attacks']:
        tag = 'School Shootings'
    if tag in ['Midland-Odessa, Tex, Shooting (2019)', 'Dayton, Ohio, Shooting (2019)', 'El Paso, Tex, Shooting (2019)', 'El Paso', 'Dayton', 'Shooting (2019)', 'Tex']:
        tag = 'Shootings'
    if 'Russian Interference in 2016' in tag:
        tag = 'Russian interference in the 2016 United States elections'
    if tag in ['Homosexuality and Bisexuality']:
        tag = 'Homosexuality'
    if 'Trump-Ukraine' in tag:
        tag = 'Trump Ukraine Whistle blower'
    if tag in ['Biden, Joseph R Jr', 'Biden']:
        tag = 'Joe Biden'
    if tag in ['Sanders, Bernard', 'Sanders', 'Bernard', 'Bernie Sanders']:
        tag = 'Bernie Sanders'
    if tag in ['Pete Buttigieg', 'Buttigieg, Pete (1982- )', 'Buttigieg', 'Pete Buttigieg', 'Pete (1982- )']:
        tag = 'Pete Buttigieg'
    if tag in ['Blacks', 'Black People']:
        tag = 'Blacks'
    if 'Shutdowns' in tag:
        tag = 'Shutdowns'
    if 'Quarantine' in tag:
        tag = 'Quarantines'
    if 'Deaths' in tag:
        tag = 'Deaths'
    if 'Child' in tag:
        tag = 'Parenting'
    if 'Syria' in tag:
        tag = 'Syria'
    if tag in ['Donald Trump', 'Weddings and Engagements', 'Impeachment', 'Senate', 'Discrimination', 'Art', 'Debates (Political)', 'Demonstrations' , 'Protests and Riots', 'Women and Girls','States (US)', 'United States', 'New York State', 'New York City', 'NYC', 'NY)', 'Primaries and Caucuses', 'United States Politics and Government', 'Politics and Government', 'Books and Literature', 'Television', 'Movies', 'Real Estate and Housing (Residential)', 'United States', 'United States International Relations', 'Primaries and Caucuses', 'United States Economy', 'Elections']:
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
                start = int(today[6:7])
            else:
                start = int(today[5:7])
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

                articles['tags'] = [''.join(tag['value']) for tag in a['keywords']]
                cleaning_List=map(cleaning_tag,  articles['tags'])
                articles['tags'] = [changed_tag for changed_tag in cleaning_List]

                monthly_article.append(articles)

            if len(str(mm)) == 1:
                mm = '0' + str(mm)
            monthly_archive[str(yy)+'-'+str(mm)] = monthly_article

            tag_arr = []
            for m in monthly_article:
                for t in m['tags']:
                    for string in t.split(', '):
                        tag_arr.append(', '.join(string.split(', ')))
            cleaning_List=map(cleaning_tag,  tag_arr)
            tag_arr = [changed_tag for changed_tag in cleaning_List]

            count_tag = {}
            for tag in tag_arr:
                if tag is not '':
                    if tag in count_tag:
                        count_tag[tag] += 1
                    else:
                        count_tag[tag] = 1   

            # This variable is what we want to get in NYTimes
            tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:10]
            frequent_tags_archive[str(yy)+'-'+str(mm)] = tags_with_frequency

    return monthly_archive, frequent_tags_archive

def call_combined_monthly_tag_by_periode(frequent_tags_archive):
    combined_monthly_tag_by_periode = {}
    for time_period in frequent_tags_archive:
        tag_only = []
        for each in frequent_tags_archive[time_period]:    
            tag_only.append(each[0])
            combined_monthly_tag_by_periode[time_period] = tag_only
    return combined_monthly_tag_by_periode

def call_overall_Unique_tag_with_frequency(frequent_tags_archive):
    overall_Unique_tag_with_frequency={}
    for periode in frequent_tags_archive:
        for tag_with_F in frequent_tags_archive[periode]:
            if tag_with_F[0] in overall_Unique_tag_with_frequency:
                overall_Unique_tag_with_frequency[tag_with_F[0]] = tag_with_F[1] + overall_Unique_tag_with_frequency[tag_with_F[0]]
            else:
                overall_Unique_tag_with_frequency[tag_with_F[0]] = tag_with_F[1]

    overall_Unique_tag_with_frequency = sorted(overall_Unique_tag_with_frequency.items(),key=operator.itemgetter(1),reverse=True)
    return overall_Unique_tag_with_frequency



#####################################################
# Create a Class for Fetching 3 different endpoints #
#####################################################

class Fetcher(object):

    def store_times(self, monthly_archive, frequent_tags_archive, session):
        multi_articles = {}
        for periode in frequent_tags_archive:
            print('periode : ', periode)     
            for top_tag in frequent_tags_archive[periode]:
                # Get specific NYTimes article information per each tags
                # print('* * : ', monthly_archive[periode])
                for each in monthly_archive[periode]:
                    if top_tag[0] in multi_articles and periode in multi_articles[top_tag[0]]:
                        pass                             
                    else:
                        # print(top_tag[0] in each['tags'])
                        if len(each['tags']) != 0 and top_tag[0] in each['tags']:
                            try:
                                print('date : ', each['pub_date']) 
                                insert_TimesTag = TimesTable(
                                    tag=top_tag[0],
                                    periodeM=periode,
                                    frequency=top_tag[1],
                                    title=each['title'],
                                    date=each['pub_date'],
                                    url=each['url'],
                                    img_URL=each['thm_img'])

                                multi_articles[top_tag[0]] = periode

                                session.add(insert_TimesTag)
                                session.flush()
                            except Exception as e:
                                print(" = Unable insert_TimesTag to DB : ", top_tag[0], periode, " =", e)
                                pass   
                     
    def store_google(self, combined_monthly_tag, session):
        today = str(datetime.today())
        # Connect with Pytrend(Google Search Trend), to get Search Interest Index
        pytrends = TrendReq(hl='en-US', tz=360)

        for periode in combined_monthly_tag:
            add_post_arr = []

            for top_tag in combined_monthly_tag[periode]:
                tag_arr = []
                tag_arr.append(top_tag)
                interest_over_time = {}
                
                try:
                    time.sleep(3)
                    pytrends.build_payload(tag_arr, cat=0, timeframe = '2019-05-01 '+ today[:10], geo='', gprop='')
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
                    print(" = Unable insert_Google to DB : ", top_tag, e, " =")
                    pass

    def call_Youtube(self, unique_tag_only_with_frequency):
        # creating Youtube Resource Object 
        youtube_object = discovery.build(Youtube_service_name, Youtube_API_version, developerKey = Youtube_developer_key)
        
        max_results = 10
        youtube_metadata = []
        
        for tag_frequency in unique_tag_only_with_frequency:
            viewCount = 0
            commentCount = 0
            likeCount = 0
            turned_off_comments = 0
            
            video = {}
            contain_stats = {}
            
            time.sleep(6)
            search_tags = youtube_object.search().list(q = tag_frequency[0], part = "id, snippet", order = 'relevance', maxResults = max_results, publishedAfter = "2020-01-01T00:00:00Z").execute() 
            time.sleep(3)
            
            for item in search_tags.get("items", []):
                try:
                    time.sleep(3)
                    stats = youtube_object.videos().list(part='statistics, snippet', id=item["id"]["videoId"]).execute()
                    time.sleep(3)
                    viewCount = int(stats.get("items", [])[0]['statistics']['viewCount'])
                    likeCount =  int(stats.get("items", [])[0]['statistics']['likeCount'])
                    commentCount = int(stats.get("items", [])[0]['statistics']['commentCount'])

                except Exception as e:
                    print(" = Unable search Youtube : ", tag_frequency[0], " =", e)
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
                
                if tag_frequency[0] in video.keys():
                    pass
                else:
                    video[tag_frequency[0]] = contain_stats       
            youtube_metadata.append(video)   
        return youtube_metadata

    def store_youtube(self, youtube_metadata, session):
        for each_youtube in youtube_metadata:
            unique_tag = list(each_youtube.keys())[0]
            try:
                insert_Youtube = YoutubeTable(
                    tag=unique_tag,
                    viewCount=each_youtube[unique_tag]['viewCount'],
                    commentCount=each_youtube[unique_tag]['commentCount'],
                    likeCount=each_youtube[unique_tag]['likeCount']
                )
                session.add(insert_Youtube)
                session.flush()
            except Exception as e:
                print(" = Unable insert_Youtube to DB : ", each_youtube['tag'], " =", e)
                pass

    def store_rest_data(self, monthly_archive, combined_monthly_tag_by_periode, overall_Unique_tag_with_frequency, session):
        try:
            for periode in monthly_archive:
                insert_monthly_archive = MonthlyTagTable(
                    periodeM = periode,
                    article_archives = monthly_archive[periode]
                    )
                session.add(insert_monthly_archive)

            for periode in combined_monthly_tag_by_periode.keys():
                insert_combined_monthly_tag_by_periode = TagByPeriodeTable(
                    periodeM = periode,
                    tagArr_per_month = combined_monthly_tag_by_periode[periode]
                    )
                session.add(insert_combined_monthly_tag_by_periode)

            for tag_frequency in overall_Unique_tag_with_frequency:
                insert_overall_Unique_tag_with_frequency = UniqueTagNFrequencyTable(
                    tag = tag_frequency[0],
                    frequency = tag_frequency[1]
                    )
                session.add(insert_overall_Unique_tag_with_frequency)

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
    combined_monthly_tag_by_periode = call_combined_monthly_tag_by_periode(frequent_tags_archive)
    overall_Unique_tag_with_frequency = call_overall_Unique_tag_with_frequency(frequent_tags_archive)

    try:
        f1 = Fetcher()
        f1.store_times(monthly_archive, frequent_tags_archive, session)
        f1.store_google(combined_monthly_tag_by_periode, session)

        youtube_metadata = f1.call_Youtube(overall_Unique_tag_with_frequency)
        f1.store_youtube(youtube_metadata, session)
        f1.store_rest_data(monthly_archive, combined_monthly_tag_by_periode, overall_Unique_tag_with_frequency, session)    
        session.commit()
    except Exception as e:
        print('= Cannot store into DB, why? =', e)
    finally:
        session.close()


run_all_fetch()