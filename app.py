import os
import sys
import configparser
import datetime
import requests
import operator

from pandas.io.json import json_normalize
from flask import Flask, jsonify, render_template, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, distinct
from flask_sqlalchemy import SQLAlchemy


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


###############
# Flask Setup #
###############

app = Flask(__name__)


############
# Database #
############

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monthly_times_tags.db'
db = SQLAlchemy(app)

################
# Define Model #
################


class TimesData(db.Model): 
    __tablename__ = 'times'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(25))
    Tag = db.Column(db.String(255))
    Frequency = db.Column(db.String(255))
    Title = db.Column(db.String(255))
    Date = db.Column(db.String(25))
    Url = db.Column(db.String(255))
    img_URL = db.Column(db.String(255))

class GoogleData(db.Model): 
    __tablename__ = 'google'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(25))
    Tag = db.Column(db.String(25))
    Date_0 = db.Column(db.String(25))
    Rate_0 = db.Column(db.Integer)
    Date_1 = db.Column(db.String(25))
    Rate_1 = db.Column(db.Integer)
    Date_2 = db.Column(db.String(25))
    Rate_2 = db.Column(db.Integer)
    Date_3 = db.Column(db.String(25))
    Rate_3 = db.Column(db.Integer)
    Date_4 = db.Column(db.String(25))
    Rate_4 = db.Column(db.Integer)
    Date_5 = db.Column(db.String(25))
    Rate_5 = db.Column(db.Integer)
    Date_6 = db.Column(db.String(25))
    Rate_6 = db.Column(db.Integer)
    Date_7 = db.Column(db.String(25))
    Rate_7 = db.Column(db.Integer)
    Date_8 = db.Column(db.String(25))
    Rate_8 = db.Column(db.Integer)
    Date_9 = db.Column(db.String(25))
    Rate_9 = db.Column(db.Integer)
    Date_10 = db.Column(db.String(25))
    Rate_10 = db.Column(db.Integer)
    Date_11 = db.Column(db.String(25))
    Rate_11 = db.Column(db.Integer)
    Date_12 = db.Column(db.String(25))
    Rate_12 = db.Column(db.Integer)
    Date_13 = db.Column(db.String(25))
    Rate_13 = db.Column(db.Integer)
    Date_14 = db.Column(db.String(25))
    Rate_14 = db.Column(db.Integer)
    Date_15 = db.Column(db.String(25))
    Rate_15 = db.Column(db.Integer)
    Date_16 = db.Column(db.String(25))
    Rate_16 = db.Column(db.Integer)
    Date_17 = db.Column(db.String(25))
    Rate_17 = db.Column(db.Integer)
    Busiest_date = db.Column(db.String(25))
    Date_18 = db.Column(db.String(25))
    Rate_18 = db.Column(db.Integer)
    Date_19 = db.Column(db.String(25))
    Rate_19 = db.Column(db.Integer)
    Date_20 = db.Column(db.String(25))
    Rate_20 = db.Column(db.Integer)
    Date_21 = db.Column(db.String(25))
    Rate_21 = db.Column(db.Integer)
    Date_22 = db.Column(db.String(25))
    Rate_22 = db.Column(db.Integer)
    Date_23 = db.Column(db.String(25))
    Rate_23 = db.Column(db.Integer)
    Date_24 = db.Column(db.String(25))
    Rate_24 = db.Column(db.Integer)
    Date_25 = db.Column(db.String(25))
    Rate_25 = db.Column(db.Integer)
    Date_26 = db.Column(db.String(25))
    Rate_26 = db.Column(db.Integer)
    Date_27 = db.Column(db.String(25))
    Rate_27 = db.Column(db.Integer)
    Date_28 = db.Column(db.String(25))
    Rate_28 = db.Column(db.Integer)
    Date_29 = db.Column(db.String(25))
    Rate_29 = db.Column(db.Integer)
    Date_30 = db.Column(db.String(25))
    Rate_30 = db.Column(db.Integer)
    Date_31 = db.Column(db.String(25))
    Rate_31 = db.Column(db.Integer)
    Date_32 = db.Column(db.String(25))
    Rate_32 = db.Column(db.Integer)
    Date_33 = db.Column(db.String(25))
    Rate_33 = db.Column(db.Integer)
    Date_34 = db.Column(db.String(25))
    Rate_34 = db.Column(db.Integer)
    Date_35 = db.Column(db.String(25))
    Rate_35 = db.Column(db.Integer)
    Date_36 = db.Column(db.String(25))
    Rate_36 = db.Column(db.Integer)
    Date_37 = db.Column(db.String(25))
    Rate_37 = db.Column(db.Integer)
    Date_38 = db.Column(db.String(25))
    Rate_38 = db.Column(db.Integer)
    Date_39 = db.Column(db.String(25))
    Rate_39 = db.Column(db.Integer)
    Date_40 = db.Column(db.String(25))
    Rate_40 = db.Column(db.Integer)
    Date_41 = db.Column(db.String(25))
    Rate_41 = db.Column(db.Integer)
    Date_42 = db.Column(db.String(25))
    Rate_42 = db.Column(db.Integer)
    Date_43 = db.Column(db.String(25))
    Rate_43 = db.Column(db.Integer)
    Date_44 = db.Column(db.String(25))
    Rate_44 = db.Column(db.Integer)
    Date_45 = db.Column(db.String(25))
    Rate_45 = db.Column(db.Integer)
    Date_46 = db.Column(db.String(25))
    Rate_46 = db.Column(db.Integer)
    Date_47 = db.Column(db.String(25))
    Rate_47 = db.Column(db.Integer)
    Date_48 = db.Column(db.String(25))
    Rate_48 = db.Column(db.Integer)
    Date_49 = db.Column(db.String(25))
    Rate_49 = db.Column(db.Integer)
    Date_50 = db.Column(db.String(25))
    Rate_50 = db.Column(db.Integer)
    Date_51 = db.Column(db.String(25))
    Rate_51 = db.Column(db.Integer)
    Date_52 = db.Column(db.String(25))
    Rate_52 = db.Column(db.Integer)
    Date_53 = db.Column(db.String(25))
    Rate_53 = db.Column(db.Integer)
    Date_54 = db.Column(db.String(25))
    Rate_54 = db.Column(db.Integer)
    Date_55 = db.Column(db.String(25))
    Rate_55 = db.Column(db.Integer)
    Date_56 = db.Column(db.String(25))
    Rate_56 = db.Column(db.Integer)
    Date_57 = db.Column(db.String(25))
    Rate_57 = db.Column(db.Integer)
    Date_58 = db.Column(db.String(25))
    Rate_58 = db.Column(db.Integer)
    Date_59 = db.Column(db.String(25))
    Rate_59 = db.Column(db.Integer)
    Date_60 = db.Column(db.String(25))
    Rate_60 = db.Column(db.Integer)
    Date_61 = db.Column(db.String(25))
    Rate_61 = db.Column(db.Integer)
    Date_62 = db.Column(db.String(25))
    Rate_62 = db.Column(db.Integer)
    Date_63 = db.Column(db.String(25))
    Rate_63 = db.Column(db.Integer)
    Date_64 = db.Column(db.String(25))
    Rate_64 = db.Column(db.Integer)
    Date_65 = db.Column(db.String(25))
    Rate_65 = db.Column(db.Integer)
    Date_66 = db.Column(db.String(25))
    Rate_66 = db.Column(db.Integer)
    Date_67 = db.Column(db.String(25))
    Rate_67 = db.Column(db.Integer)
    Date_68 = db.Column(db.String(25))
    Rate_68 = db.Column(db.Integer)
    Date_69 = db.Column(db.String(25))
    Rate_69 = db.Column(db.Integer)
    Date_70 = db.Column(db.String(25))
    Rate_70 = db.Column(db.Integer)
    Date_71 = db.Column(db.String(25))
    Rate_71 = db.Column(db.Integer)
    Date_72 = db.Column(db.String(25))
    Rate_72 = db.Column(db.Integer)
    Date_73 = db.Column(db.String(25))
    Rate_73 = db.Column(db.Integer)
    Date_74 = db.Column(db.String(25))
    Rate_74 = db.Column(db.Integer)
    Date_75 = db.Column(db.String(25))
    Rate_75 = db.Column(db.Integer)
    Date_76 = db.Column(db.String(25))
    Rate_76 = db.Column(db.Integer)
    Date_77 = db.Column(db.String(25))
    Rate_77 = db.Column(db.Integer)
    Date_78 = db.Column(db.String(25))
    Rate_78 = db.Column(db.Integer)
    Date_79 = db.Column(db.String(25))
    Rate_79 = db.Column(db.Integer)
    Date_80 = db.Column(db.String(25))
    Rate_80 = db.Column(db.Integer)
    Date_81 = db.Column(db.String(25))
    Rate_81 = db.Column(db.Integer)
    Date_82 = db.Column(db.String(25))
    Rate_82 = db.Column(db.Integer)
    Date_83 = db.Column(db.String(25))
    Rate_83 = db.Column(db.Integer)
    Date_84 = db.Column(db.String(25))
    Rate_84 = db.Column(db.Integer)
    Date_85 = db.Column(db.String(25))
    Rate_85 = db.Column(db.Integer)
    Date_86 = db.Column(db.String(25))
    Rate_86 = db.Column(db.Integer)
    Date_87 = db.Column(db.String(25))
    Rate_87 = db.Column(db.Integer)
    Date_88 = db.Column(db.String(25))
    Rate_88 = db.Column(db.Integer)
    Date_89 = db.Column(db.String(25))
    Rate_89 = db.Column(db.Integer)
    Date_90 = db.Column(db.String(25))
    Rate_90 = db.Column(db.Integer)
    Date_91 = db.Column(db.String(25))
    Rate_91 = db.Column(db.Integer)
    Date_92 = db.Column(db.String(25))
    Rate_92 = db.Column(db.Integer)
    Date_93 = db.Column(db.String(25))
    Rate_93 = db.Column(db.Integer)
    Date_94 = db.Column(db.String(25))
    Rate_94 = db.Column(db.Integer)
    Date_95 = db.Column(db.String(25))
    Rate_95 = db.Column(db.Integer)
    Date_96 = db.Column(db.String(25))
    Rate_96 = db.Column(db.Integer)
    Date_97 = db.Column(db.String(25))
    Rate_97 = db.Column(db.Integer)
    Date_98 = db.Column(db.String(25))
    Rate_98 = db.Column(db.Integer)
    Date_99 = db.Column(db.String(25))
    Rate_99 = db.Column(db.Integer)
    Date_100 = db.Column(db.String(25))
    Rate_100 = db.Column(db.Integer)
    Date_101 = db.Column(db.String(25))
    Rate_101 = db.Column(db.Integer)
    Date_102 = db.Column(db.String(25))
    Rate_102 = db.Column(db.Integer)
    Date_103 = db.Column(db.String(25))
    Rate_103 = db.Column(db.Integer)
    Date_104 = db.Column(db.String(25))
    Rate_104 = db.Column(db.Integer)
    Date_105 = db.Column(db.String(25))
    Rate_105 = db.Column(db.Integer)
    Date_106 = db.Column(db.String(25))
    Rate_106 = db.Column(db.Integer)
    Date_107 = db.Column(db.String(25))
    Rate_107 = db.Column(db.Integer)
    Date_108 = db.Column(db.String(25))
    Rate_108 = db.Column(db.Integer)
    Date_109 = db.Column(db.String(25))
    Rate_109 = db.Column(db.Integer)
    Date_110 = db.Column(db.String(25))
    Rate_110 = db.Column(db.Integer)
    Date_111 = db.Column(db.String(25))
    Rate_111 = db.Column(db.Integer)
    Date_112 = db.Column(db.String(25))
    Rate_112 = db.Column(db.Integer)
    Date_113 = db.Column(db.String(25))
    Rate_113 = db.Column(db.Integer)
    Date_114 = db.Column(db.String(25))
    Rate_114 = db.Column(db.Integer)
    Date_115 = db.Column(db.String(25))
    Rate_115 = db.Column(db.Integer)
    Date_116 = db.Column(db.String(25))
    Rate_116 = db.Column(db.Integer)
    Date_117 = db.Column(db.String(25))
    Rate_117 = db.Column(db.Integer)

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
    results = db.session.query(
        TimesData.Category,
        TimesData.Tag,
        TimesData.Frequency,
        TimesData.Title,
        TimesData.Date,
        TimesData.Url,
        TimesData.img_URL
    ).all()

    db.session.close()

    # Results of the query
    times_metadata = []
    for Category, Tag, Frequency, Title, Date, Url, img_URL in results:
        each_metadata = {}
        each_metadata['Category'] = Category
        each_metadata['Tag'] = Tag
        each_metadata['Frequency'] = Frequency
        each_metadata['Title'] = Title
        each_metadata['Date'] = Date
        each_metadata['Url'] = Url
        each_metadata['img_URL'] = img_URL
        times_metadata.append(each_metadata)


    return jsonify(times_metadata)


# Get Times Metadata 
@app.route("/google")
def Google():
    # Create session and query all data
    results = db.session.query(GoogleData.Category, GoogleData.Tag, GoogleData.Date_0, GoogleData.Rate_0 , GoogleData.Date_1, GoogleData.Rate_1 , GoogleData.Date_2, GoogleData.Rate_2 , GoogleData.Date_3, GoogleData.Rate_3 , GoogleData.Date_4, GoogleData.Rate_4 , GoogleData.Date_5, GoogleData.Rate_5 , GoogleData.Date_6, GoogleData.Rate_6 , GoogleData.Date_7, GoogleData.Rate_7 , GoogleData.Date_8, GoogleData.Rate_8 , GoogleData.Date_9, GoogleData.Rate_9 , GoogleData.Date_10, GoogleData.Rate_10 , GoogleData.Date_11, GoogleData.Rate_11 , GoogleData.Date_12, GoogleData.Rate_12 , GoogleData.Date_13, GoogleData.Rate_13 , GoogleData.Date_14, GoogleData.Rate_14 , GoogleData.Date_15, GoogleData.Rate_15 , GoogleData.Date_16, GoogleData.Rate_16 , GoogleData.Date_17, GoogleData.Rate_17 , GoogleData.Busiest_date, GoogleData.Date_18, GoogleData.Rate_18 , GoogleData.Date_19, GoogleData.Rate_19 , GoogleData.Date_20, GoogleData.Rate_20 , GoogleData.Date_21, GoogleData.Rate_21 , GoogleData.Date_22, GoogleData.Rate_22 , GoogleData.Date_23, GoogleData.Rate_23 , GoogleData.Date_24, GoogleData.Rate_24 , GoogleData.Date_25, GoogleData.Rate_25 , GoogleData.Date_26, GoogleData.Rate_26 , GoogleData.Date_27, GoogleData.Rate_27 , GoogleData.Date_28, GoogleData.Rate_28 , GoogleData.Date_29, GoogleData.Rate_29 , GoogleData.Date_30, GoogleData.Rate_30 , GoogleData.Date_31, GoogleData.Rate_31 , GoogleData.Date_32, GoogleData.Rate_32 , GoogleData.Date_33, GoogleData.Rate_33 , GoogleData.Date_34, GoogleData.Rate_34 , GoogleData.Date_35, GoogleData.Rate_35 , GoogleData.Date_36, GoogleData.Rate_36 , GoogleData.Date_37, GoogleData.Rate_37 , GoogleData.Date_38, GoogleData.Rate_38 , GoogleData.Date_39, GoogleData.Rate_39 , GoogleData.Date_40, GoogleData.Rate_40 , GoogleData.Date_41, GoogleData.Rate_41 , GoogleData.Date_42, GoogleData.Rate_42 , GoogleData.Date_43, GoogleData.Rate_43 , GoogleData.Date_44, GoogleData.Rate_44 , GoogleData.Date_45, GoogleData.Rate_45 , GoogleData.Date_46, GoogleData.Rate_46 , GoogleData.Date_47, GoogleData.Rate_47 , GoogleData.Date_48, GoogleData.Rate_48 , GoogleData.Date_49, GoogleData.Rate_49 , GoogleData.Date_50, GoogleData.Rate_50 , GoogleData.Date_51, GoogleData.Rate_51 , GoogleData.Date_52, GoogleData.Rate_52 , GoogleData.Date_53, GoogleData.Rate_53 , GoogleData.Date_54, GoogleData.Rate_54 , GoogleData.Date_55, GoogleData.Rate_55 , GoogleData.Date_56, GoogleData.Rate_56 , GoogleData.Date_57, GoogleData.Rate_57 , GoogleData.Date_58, GoogleData.Rate_58 , GoogleData.Date_59, GoogleData.Rate_59 , GoogleData.Date_60, GoogleData.Rate_60 , GoogleData.Date_61, GoogleData.Rate_61 , GoogleData.Date_62, GoogleData.Rate_62 , GoogleData.Date_63, GoogleData.Rate_63 , GoogleData.Date_64, GoogleData.Rate_64 , GoogleData.Date_65, GoogleData.Rate_65 , GoogleData.Date_66, GoogleData.Rate_66 , GoogleData.Date_67, GoogleData.Rate_67 , GoogleData.Date_68, GoogleData.Rate_68 , GoogleData.Date_69, GoogleData.Rate_69 , GoogleData.Date_70, GoogleData.Rate_70 , GoogleData.Date_71, GoogleData.Rate_71 , GoogleData.Date_72, GoogleData.Rate_72 , GoogleData.Date_73, GoogleData.Rate_73 , GoogleData.Date_74, GoogleData.Rate_74 , GoogleData.Date_75, GoogleData.Rate_75 , GoogleData.Date_76, GoogleData.Rate_76 , GoogleData.Date_77, GoogleData.Rate_77 , GoogleData.Date_78, GoogleData.Rate_78 , GoogleData.Date_79, GoogleData.Rate_79 , GoogleData.Date_80, GoogleData.Rate_80 , GoogleData.Date_81, GoogleData.Rate_81 , GoogleData.Date_82, GoogleData.Rate_82 , GoogleData.Date_83, GoogleData.Rate_83 , GoogleData.Date_84, GoogleData.Rate_84 , GoogleData.Date_85, GoogleData.Rate_85 , GoogleData.Date_86, GoogleData.Rate_86 , GoogleData.Date_87, GoogleData.Rate_87 , GoogleData.Date_88, GoogleData.Rate_88 , GoogleData.Date_89, GoogleData.Rate_89 , GoogleData.Date_90, GoogleData.Rate_90 , GoogleData.Date_91, GoogleData.Rate_91 , GoogleData.Date_92, GoogleData.Rate_92 , GoogleData.Date_93, GoogleData.Rate_93 , GoogleData.Date_94, GoogleData.Rate_94 , GoogleData.Date_95, GoogleData.Rate_95 , GoogleData.Date_96, GoogleData.Rate_96 , GoogleData.Date_97, GoogleData.Rate_97 , GoogleData.Date_98, GoogleData.Rate_98 , GoogleData.Date_99, GoogleData.Rate_99 , GoogleData.Date_100, GoogleData.Rate_100 , GoogleData.Date_101, GoogleData.Rate_101 , GoogleData.Date_102, GoogleData.Rate_102 , GoogleData.Date_103, GoogleData.Rate_103 , GoogleData.Date_104, GoogleData.Rate_104 , GoogleData.Date_105, GoogleData.Rate_105 , GoogleData.Date_106, GoogleData.Rate_106 , GoogleData.Date_107, GoogleData.Rate_107 , GoogleData.Date_108, GoogleData.Rate_108 , GoogleData.Date_109, GoogleData.Rate_109 , GoogleData.Date_110, GoogleData.Rate_110 , GoogleData.Date_111, GoogleData.Rate_111 , GoogleData.Date_112, GoogleData.Rate_112 , GoogleData.Date_113, GoogleData.Rate_113 , GoogleData.Date_114, GoogleData.Rate_114 , GoogleData.Date_115, GoogleData.Rate_115 , GoogleData.Date_116, GoogleData.Rate_116 , GoogleData.Date_117, GoogleData.Rate_117).all()

    db.session.close()

    # Results of the query
    google_interest = []
    for Category, Tag, Date_0, Rate_0 , Date_1, Rate_1 , Date_2, Rate_2 , Date_3, Rate_3 , Date_4, Rate_4 , Date_5, Rate_5 , Date_6, Rate_6 , Date_7, Rate_7 , Date_8, Rate_8 , Date_9, Rate_9 , Date_10, Rate_10 , Date_11, Rate_11 , Date_12, Rate_12 , Date_13, Rate_13 , Date_14, Rate_14 , Date_15, Rate_15 , Date_16, Rate_16 , Date_17, Rate_17 , Busiest_date, Date_18, Rate_18 , Date_19, Rate_19 , Date_20, Rate_20 , Date_21, Rate_21 , Date_22, Rate_22 , Date_23, Rate_23 , Date_24, Rate_24 , Date_25, Rate_25 , Date_26, Rate_26 , Date_27, Rate_27 , Date_28, Rate_28 , Date_29, Rate_29 , Date_30, Rate_30 , Date_31, Rate_31 , Date_32, Rate_32 , Date_33, Rate_33 , Date_34, Rate_34 , Date_35, Rate_35 , Date_36, Rate_36 , Date_37, Rate_37 , Date_38, Rate_38 , Date_39, Rate_39 , Date_40, Rate_40 , Date_41, Rate_41 , Date_42, Rate_42 , Date_43, Rate_43 , Date_44, Rate_44 , Date_45, Rate_45 , Date_46, Rate_46 , Date_47, Rate_47 , Date_48, Rate_48 , Date_49, Rate_49 , Date_50, Rate_50 , Date_51, Rate_51 , Date_52, Rate_52 , Date_53, Rate_53 , Date_54, Rate_54 , Date_55, Rate_55 , Date_56, Rate_56 , Date_57, Rate_57 , Date_58, Rate_58 , Date_59, Rate_59 , Date_60, Rate_60 , Date_61, Rate_61 , Date_62, Rate_62 , Date_63, Rate_63 , Date_64, Rate_64 , Date_65, Rate_65 , Date_66, Rate_66 , Date_67, Rate_67 , Date_68, Rate_68 , Date_69, Rate_69 , Date_70, Rate_70 , Date_71, Rate_71 , Date_72, Rate_72 , Date_73, Rate_73 , Date_74, Rate_74 , Date_75, Rate_75 , Date_76, Rate_76 , Date_77, Rate_77 , Date_78, Rate_78 , Date_79, Rate_79 , Date_80, Rate_80 , Date_81, Rate_81 , Date_82, Rate_82 , Date_83, Rate_83 , Date_84, Rate_84 , Date_85, Rate_85 , Date_86, Rate_86 , Date_87, Rate_87 , Date_88, Rate_88 , Date_89, Rate_89 , Date_90, Rate_90 , Date_91, Rate_91 , Date_92, Rate_92 , Date_93, Rate_93 , Date_94, Rate_94 , Date_95, Rate_95 , Date_96, Rate_96 , Date_97, Rate_97 , Date_98, Rate_98 , Date_99, Rate_99 , Date_100, Rate_100 , Date_101, Rate_101 , Date_102, Rate_102 , Date_103, Rate_103 , Date_104, Rate_104 , Date_105, Rate_105 , Date_106, Rate_106 , Date_107, Rate_107 , Date_108, Rate_108 , Date_109, Rate_109 , Date_110, Rate_110 , Date_111, Rate_111 , Date_112, Rate_112 , Date_113, Rate_113 , Date_114, Rate_114 , Date_115, Rate_115 , Date_116, Rate_116 , Date_117, Rate_117 in results:
        each_interest = {}
        each_interest['Category'] = Category
        each_interest['Tag'] = Tag
        each_interest['Busiest_date'] = Busiest_date
        each_interest['Date_0'] = Date_0  
        each_interest['Rate_0'] = Rate_0  
        each_interest['Date_1'] = Date_1  
        each_interest['Rate_1'] = Rate_1  
        each_interest['Date_2'] = Date_2  
        each_interest['Rate_2'] = Rate_2  
        each_interest['Date_3'] = Date_3  
        each_interest['Rate_3'] = Rate_3  
        each_interest['Date_4'] = Date_4  
        each_interest['Rate_4'] = Rate_4  
        each_interest['Date_5'] = Date_5  
        each_interest['Rate_5'] = Rate_5  
        each_interest['Date_6'] = Date_6  
        each_interest['Rate_6'] = Rate_6  
        each_interest['Date_7'] = Date_7  
        each_interest['Rate_7'] = Rate_7  
        each_interest['Date_8'] = Date_8  
        each_interest['Rate_8'] = Rate_8  
        each_interest['Date_9'] = Date_9  
        each_interest['Rate_9'] = Rate_9  
        each_interest['Date_10'] = Date_10 
        each_interest['Rate_10'] = Rate_10  
        each_interest['Date_11'] = Date_11 
        each_interest['Rate_11'] = Rate_11  
        each_interest['Date_12'] = Date_12 
        each_interest['Rate_12'] = Rate_12  
        each_interest['Date_13'] = Date_13 
        each_interest['Rate_13'] = Rate_13  
        each_interest['Date_14'] = Date_14 
        each_interest['Rate_14'] = Rate_14  
        each_interest['Date_15'] = Date_15 
        each_interest['Rate_15'] = Rate_15  
        each_interest['Date_16'] = Date_16 
        each_interest['Rate_16'] = Rate_16  
        each_interest['Date_17'] = Date_17 
        each_interest['Rate_17'] = Rate_17  
        each_interest['Date_18'] = Date_18 
        each_interest['Rate_18'] = Rate_18  
        each_interest['Date_19'] = Date_19 
        each_interest['Rate_19'] = Rate_19  
        each_interest['Date_20'] = Date_20 
        each_interest['Rate_20'] = Rate_20  
        each_interest['Date_21'] = Date_21 
        each_interest['Rate_21'] = Rate_21  
        each_interest['Date_22'] = Date_22 
        each_interest['Rate_22'] = Rate_22  
        each_interest['Date_23'] = Date_23 
        each_interest['Rate_23'] = Rate_23  
        each_interest['Date_24'] = Date_24 
        each_interest['Rate_24'] = Rate_24  
        each_interest['Date_25'] = Date_25 
        each_interest['Rate_25'] = Rate_25  
        each_interest['Date_26'] = Date_26 
        each_interest['Rate_26'] = Rate_26  
        each_interest['Date_27'] = Date_27 
        each_interest['Rate_27'] = Rate_27  
        each_interest['Date_28'] = Date_28 
        each_interest['Rate_28'] = Rate_28  
        each_interest['Date_29'] = Date_29 
        each_interest['Rate_29'] = Rate_29  
        each_interest['Date_30'] = Date_30 
        each_interest['Rate_30'] = Rate_30  
        each_interest['Date_31'] = Date_31 
        each_interest['Rate_31'] = Rate_31  
        each_interest['Date_32'] = Date_32 
        each_interest['Rate_32'] = Rate_32  
        each_interest['Date_33'] = Date_33 
        each_interest['Rate_33'] = Rate_33  
        each_interest['Date_34'] = Date_34 
        each_interest['Rate_34'] = Rate_34  
        each_interest['Date_35'] = Date_35 
        each_interest['Rate_35'] = Rate_35  
        each_interest['Date_36'] = Date_36 
        each_interest['Rate_36'] = Rate_36  
        each_interest['Date_37'] = Date_37 
        each_interest['Rate_37'] = Rate_37  
        each_interest['Date_38'] = Date_38 
        each_interest['Rate_38'] = Rate_38  
        each_interest['Date_39'] = Date_39 
        each_interest['Rate_39'] = Rate_39  
        each_interest['Date_40'] = Date_40 
        each_interest['Rate_40'] = Rate_40  
        each_interest['Date_41'] = Date_41 
        each_interest['Rate_41'] = Rate_41  
        each_interest['Date_42'] = Date_42 
        each_interest['Rate_42'] = Rate_42  
        each_interest['Date_43'] = Date_43 
        each_interest['Rate_43'] = Rate_43  
        each_interest['Date_44'] = Date_44 
        each_interest['Rate_44'] = Rate_44  
        each_interest['Date_45'] = Date_45 
        each_interest['Rate_45'] = Rate_45  
        each_interest['Date_46'] = Date_46 
        each_interest['Rate_46'] = Rate_46  
        each_interest['Date_47'] = Date_47 
        each_interest['Rate_47'] = Rate_47  
        each_interest['Date_48'] = Date_48 
        each_interest['Rate_48'] = Rate_48  
        each_interest['Date_49'] = Date_49 
        each_interest['Rate_49'] = Rate_49  
        each_interest['Date_50'] = Date_50 
        each_interest['Rate_50'] = Rate_50  
        each_interest['Date_51'] = Date_51 
        each_interest['Rate_51'] = Rate_51  
        each_interest['Date_52'] = Date_52 
        each_interest['Rate_52'] = Rate_52  
        each_interest['Date_53'] = Date_53 
        each_interest['Rate_53'] = Rate_53  
        each_interest['Date_54'] = Date_54 
        each_interest['Rate_54'] = Rate_54  
        each_interest['Date_55'] = Date_55 
        each_interest['Rate_55'] = Rate_55  
        each_interest['Date_56'] = Date_56 
        each_interest['Rate_56'] = Rate_56  
        each_interest['Date_57'] = Date_57 
        each_interest['Rate_57'] = Rate_57  
        each_interest['Date_58'] = Date_58 
        each_interest['Rate_58'] = Rate_58  
        each_interest['Date_59'] = Date_59 
        each_interest['Rate_59'] = Rate_59  
        each_interest['Date_60'] = Date_60 
        each_interest['Rate_60'] = Rate_60  
        each_interest['Date_61'] = Date_61 
        each_interest['Rate_61'] = Rate_61  
        each_interest['Date_62'] = Date_62 
        each_interest['Rate_62'] = Rate_62  
        each_interest['Date_63'] = Date_63 
        each_interest['Rate_63'] = Rate_63  
        each_interest['Date_64'] = Date_64 
        each_interest['Rate_64'] = Rate_64  
        each_interest['Date_65'] = Date_65 
        each_interest['Rate_65'] = Rate_65  
        each_interest['Date_66'] = Date_66 
        each_interest['Rate_66'] = Rate_66  
        each_interest['Date_67'] = Date_67 
        each_interest['Rate_67'] = Rate_67  
        each_interest['Date_68'] = Date_68 
        each_interest['Rate_68'] = Rate_68  
        each_interest['Date_69'] = Date_69 
        each_interest['Rate_69'] = Rate_69  
        each_interest['Date_70'] = Date_70 
        each_interest['Rate_70'] = Rate_70  
        each_interest['Date_71'] = Date_71 
        each_interest['Rate_71'] = Rate_71  
        each_interest['Date_72'] = Date_72 
        each_interest['Rate_72'] = Rate_72  
        each_interest['Date_73'] = Date_73 
        each_interest['Rate_73'] = Rate_73  
        each_interest['Date_74'] = Date_74 
        each_interest['Rate_74'] = Rate_74  
        each_interest['Date_75'] = Date_75 
        each_interest['Rate_75'] = Rate_75  
        each_interest['Date_76'] = Date_76 
        each_interest['Rate_76'] = Rate_76  
        each_interest['Date_77'] = Date_77 
        each_interest['Rate_77'] = Rate_77  
        each_interest['Date_78'] = Date_78 
        each_interest['Rate_78'] = Rate_78  
        each_interest['Date_79'] = Date_79 
        each_interest['Rate_79'] = Rate_79  
        each_interest['Date_80'] = Date_80 
        each_interest['Rate_80'] = Rate_80  
        each_interest['Date_81'] = Date_81 
        each_interest['Rate_81'] = Rate_81  
        each_interest['Date_82'] = Date_82 
        each_interest['Rate_82'] = Rate_82  
        each_interest['Date_83'] = Date_83 
        each_interest['Rate_83'] = Rate_83  
        each_interest['Date_84'] = Date_84 
        each_interest['Rate_84'] = Rate_84  
        each_interest['Date_85'] = Date_85 
        each_interest['Rate_85'] = Rate_85  
        each_interest['Date_86'] = Date_86 
        each_interest['Rate_86'] = Rate_86  
        each_interest['Date_87'] = Date_87 
        each_interest['Rate_87'] = Rate_87  
        each_interest['Date_88'] = Date_88 
        each_interest['Rate_88'] = Rate_88  
        each_interest['Date_89'] = Date_89 
        each_interest['Rate_89'] = Rate_89  
        each_interest['Date_90'] = Date_90 
        each_interest['Rate_90'] = Rate_90  
        each_interest['Date_91'] = Date_91 
        each_interest['Rate_91'] = Rate_91  
        each_interest['Date_92'] = Date_92 
        each_interest['Rate_92'] = Rate_92  
        each_interest['Date_93'] = Date_93 
        each_interest['Rate_93'] = Rate_93  
        each_interest['Date_94'] = Date_94 
        each_interest['Rate_94'] = Rate_94  
        each_interest['Date_95'] = Date_95 
        each_interest['Rate_95'] = Rate_95  
        each_interest['Date_96'] = Date_96 
        each_interest['Rate_96'] = Rate_96  
        each_interest['Date_97'] = Date_97 
        each_interest['Rate_97'] = Rate_97  
        each_interest['Date_98'] = Date_98 
        each_interest['Rate_98'] = Rate_98  
        each_interest['Date_99'] = Date_99 
        each_interest['Rate_99'] = Rate_99  
        each_interest['Date_100'] = Date_100
        each_interest['Rate_100'] = Rate_100 
        each_interest['Date_101'] = Date_101
        each_interest['Rate_101'] = Rate_101 
        each_interest['Date_102'] = Date_102
        each_interest['Rate_102'] = Rate_102 
        each_interest['Date_103'] = Date_103
        each_interest['Rate_103'] = Rate_103 
        each_interest['Date_104'] = Date_104
        each_interest['Rate_104'] = Rate_104 
        each_interest['Date_105'] = Date_105
        each_interest['Rate_105'] = Rate_105 
        each_interest['Date_106'] = Date_106
        each_interest['Rate_106'] = Rate_106 
        each_interest['Date_107'] = Date_107
        each_interest['Rate_107'] = Rate_107 
        each_interest['Date_108'] = Date_108
        each_interest['Rate_108'] = Rate_108 
        each_interest['Date_109'] = Date_109
        each_interest['Rate_109'] = Rate_109 
        each_interest['Date_110'] = Date_110
        each_interest['Rate_110'] = Rate_110 
        each_interest['Date_111'] = Date_111
        each_interest['Rate_111'] = Rate_111 
        each_interest['Date_112'] = Date_112
        each_interest['Rate_112'] = Rate_112 
        each_interest['Date_113'] = Date_113
        each_interest['Rate_113'] = Rate_113 
        each_interest['Date_114'] = Date_114
        each_interest['Rate_114'] = Rate_114 
        each_interest['Date_115'] = Date_115
        each_interest['Rate_115'] = Rate_115 
        each_interest['Date_116'] = Date_116
        each_interest['Rate_116'] = Rate_116 
        each_interest['Date_117'] = Date_117
        each_interest['Rate_117'] = Rate_117
        google_interest.append(each_interest)


    return jsonify(google_interest)


if __name__ == "__main__":
    app.run(debug=True)
