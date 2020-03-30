
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


# Use CofigParser to safely store the password or key
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

#get initial data API
def get_init_data(yy, mm):
    parameters = {'api-key': Times_key}           
    archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ str(yy) +'/'+ str(mm) +'.json'
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
        if tag in ['New York City', 'NYC','NY)', 'NY']:
            tag = 'New York City'
        if tag in ['Fla', 'Parkland']:
            tag = 'Parkland'                          
        if tag in count_tag:
            count_tag[tag] += 1
        else:
            count_tag[tag] = 1   
            
    tags_with_frequency = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:20]      

    data = []
    for top_tag in tags_with_frequency:
        print(top_tag[0])
        multi_articles = {}
        for each in reversed(each_metadata) :
            if top_tag[0] in multi_articles.values():
                pass      
            else:
                if len(each['tags']) != 0 and top_tag[0] in each['tags']:
                    multi_articles['tag'] = top_tag[0]    
                    multi_articles['frequency'] = str(top_tag[1])
                    multi_articles['title'] = each['title']
                    multi_articles['pub_date'] = each['pub_date']
                    multi_articles['url'] = each['url']
                    multi_articles['description'] = each['description']
                    multi_articles['thm_img'] = each['thm_img']
                    data.append(multi_articles)
    return data


# Archive API
def get_metadata_from_timesArchivedArticles(): #these arguments need to be number
    articles_metadata = {}
    today = str(datetime.datetime.now())
    for yy in range(2018, int(today[:4]) + 1):
        if str(yy) == today[:4]:
            if '0' in today[5:7]:
                ends = int(today[6:7]) + 1
            else:
                ends = int(today[5:7]) + 1
        else:
            ends = 13
        for mm in range(1,ends):
            print(yy,mm)
            parameters = {'api-key': Times_key}           
            archived_Url = 'https://api.nytimes.com/svc/archive/v1/'+ str(yy) +'/'+ str(mm) +'.json'
            archives = requests.get(archived_Url, params=parameters).json()
#             pprint.pprint(archives['response']['docs'])
            articles_all = []
            for a in archives['response']['docs']:
                articles = {}
                articles['title'] = a['headline']['main']
                articles['pub_date'] = a['pub_date'][:10]
                articles['url'] = a['web_url']
                articles['word_count'] = a['word_count']
                articles['tags'] = [''.join(tag['value']) for tag in a['keywords']]# if a['keywords'].index(tag) == 0 or a['keywords'].index(tag) == 1 or a['keywords'].index(tag) == 2]
                articles_all.append(articles)
            articles_metadata[str(yy)+'-'+str(mm)] = articles_all
    return articles_metadata


# Get frequency data
def get_frequentlyUsedTags_from_Times(articles_metadata):
    tags_with_frequency = {}
    today = str(datetime.datetime.now())
    for yy in range(2018, int(today[:4]) + 1):
        if str(yy) == today[:4]:
            if '0' in today[5:7]:
                ends = int(today[6:7]) + 1
            else:
                ends = int(today[5:7]) + 1
        else:
            ends = 13
        for mm in range(1, ends):
            for a in articles_metadata:
                if a == str(yy)+'-'+str(mm):
                    tag_arr = []
                    for each in articles_metadata[a]:
                        for t in each['tags']:
                            for string in t.split(', '):
                                 tag_arr.append(', '.join(string.split(', ')))
                    count_tag = {}
                    tags_only = []
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
                        if tag in ['Fla', 'Parkland']:
                            tag = 'Parkland'                          
                            
                        if tag in count_tag:
                            count_tag[tag] += 1
                        else:
                            count_tag[tag] = 1
                            
                    tags_with_frequency[str(yy)+'-'+str(mm)] = sorted(count_tag.items(),key=operator.itemgetter(1),reverse=True)[:10]

                    for monthly in list(tags_with_frequency.values()):
                        for countWithtag in monthly:
                            tags_only.append(countWithtag[0].replace(' (2018)', '').replace(' (2019)',''))
                    unique_tags_only = list(set(tags_only))         
    return tags_with_frequency, unique_tags_only


# Get a unique tag collection for the search query
def get_trends_from_top10_TimesTags(unique_tags_only):
    pytrends = TrendReq(hl='en-US', tz=360)
    tags_dfs = []
    print('Total unique tags: ', len(unique_tags_only))
    for tag in unique_tags_only:
        tag_arr = []
        time.sleep(1)
        tag_arr.append(tag)
        print(tag)
        pytrends.build_payload(tag_arr, cat=0, timeframe='2018-01-01 2020-03-07', geo='', gprop='')
        time.sleep(1)
        interest_df = pytrends.interest_over_time().reset_index()
        
#         sns.lineplot( x = interest_df['date'] , y = interest_df[tag], alpha = 0.8)
#         plt.legend(loc='upper left', bbox_to_anchor=(1,1))
#         plt.xticks( rotation = 90 )
        
    tags_dfs.append(interest_df)
    return tags_dfs


# Reddit API
def get_reddit_comments(tags):
    reddit = praw.Reddit(client_id = Reddit_client_id,
                         client_secret = Reddit_client_secret,
                         username = Reddit_username,
                         password = Reddit_password,
                         user_agent = Reddit_user_agent)
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
            each_tag['URL'] = post.url
            each_tag_comments = post.comments.list()
            comments_arr = []
            for comment in each_tag_comments:
                if isinstance(comment, MoreComments):
                    continue
                comments_arr.append(comment.body)
            each_tag['Comments'] = comments_arr
        reddit_metadata.append(each_tag)
    return reddit_metadata



    