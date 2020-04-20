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
    Busiest_date = db.Column(db.String(25))
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
    Date_118 = db.Column(db.String(25))
    Rate_118 = db.Column(db.Integer)
    Date_119 = db.Column(db.String(25))
    Rate_119 = db.Column(db.Integer)
    Date_120 = db.Column(db.String(25))
    Rate_120 = db.Column(db.Integer)
    Date_121 = db.Column(db.String(25))
    Rate_121 = db.Column(db.Integer)
    Date_122 = db.Column(db.String(25))
    Rate_122 = db.Column(db.Integer)
    Date_123 = db.Column(db.String(25))
    Rate_123 = db.Column(db.Integer)
    Date_124 = db.Column(db.String(25))
    Rate_124 = db.Column(db.Integer)
    Date_125 = db.Column(db.String(25))
    Rate_125 = db.Column(db.Integer)
    Date_126 = db.Column(db.String(25))
    Rate_126 = db.Column(db.Integer)
    Date_127 = db.Column(db.String(25))
    Rate_127 = db.Column(db.Integer)
    Date_128 = db.Column(db.String(25))
    Rate_128 = db.Column(db.Integer)
    Date_129 = db.Column(db.String(25))
    Rate_129 = db.Column(db.Integer)
    Date_130 = db.Column(db.String(25))
    Rate_130 = db.Column(db.Integer)
    Date_131 = db.Column(db.String(25))
    Rate_131 = db.Column(db.Integer)
    Date_132 = db.Column(db.String(25))
    Rate_132 = db.Column(db.Integer)
    Date_133 = db.Column(db.String(25))
    Rate_133 = db.Column(db.Integer)
    Date_134 = db.Column(db.String(25))
    Rate_134 = db.Column(db.Integer)
    Date_135 = db.Column(db.String(25))
    Rate_135 = db.Column(db.Integer)
    Date_136 = db.Column(db.String(25))
    Rate_136 = db.Column(db.Integer)
    Date_137 = db.Column(db.String(25))
    Rate_137 = db.Column(db.Integer)
    Date_138 = db.Column(db.String(25))
    Rate_138 = db.Column(db.Integer)
    Date_139 = db.Column(db.String(25))
    Rate_139 = db.Column(db.Integer)
    Date_140 = db.Column(db.String(25))
    Rate_140 = db.Column(db.Integer)
    Date_141 = db.Column(db.String(25))
    Rate_141 = db.Column(db.Integer)
    Date_142 = db.Column(db.String(25))
    Rate_142 = db.Column(db.Integer)
    Date_143 = db.Column(db.String(25))
    Rate_143 = db.Column(db.Integer)
    Date_144 = db.Column(db.String(25))
    Rate_144 = db.Column(db.Integer)
    Date_145 = db.Column(db.String(25))
    Rate_145 = db.Column(db.Integer)
    Date_146 = db.Column(db.String(25))
    Rate_146 = db.Column(db.Integer)
    Date_147 = db.Column(db.String(25))
    Rate_147 = db.Column(db.Integer)
    Date_148 = db.Column(db.String(25))
    Rate_148 = db.Column(db.Integer)
    Date_149 = db.Column(db.String(25))
    Rate_149 = db.Column(db.Integer)
    Date_150 = db.Column(db.String(25))
    Rate_150 = db.Column(db.Integer)
    Date_151 = db.Column(db.String(25))
    Rate_151 = db.Column(db.Integer)
    Date_152 = db.Column(db.String(25))
    Rate_152 = db.Column(db.Integer)
    Date_153 = db.Column(db.String(25))
    Rate_153 = db.Column(db.Integer)
    Date_154 = db.Column(db.String(25))
    Rate_154 = db.Column(db.Integer)
    Date_155 = db.Column(db.String(25))
    Rate_155 = db.Column(db.Integer)
    Date_156 = db.Column(db.String(25))
    Rate_156 = db.Column(db.Integer)
    Date_157 = db.Column(db.String(25))
    Rate_157 = db.Column(db.Integer)
    Date_158 = db.Column(db.String(25))
    Rate_158 = db.Column(db.Integer)
    Date_159 = db.Column(db.String(25))
    Rate_159 = db.Column(db.Integer)
    Date_160 = db.Column(db.String(25))
    Rate_160 = db.Column(db.Integer)
    Date_161 = db.Column(db.String(25))
    Rate_161 = db.Column(db.Integer)
    Date_162 = db.Column(db.String(25))
    Rate_162 = db.Column(db.Integer)
    Date_163 = db.Column(db.String(25))
    Rate_163 = db.Column(db.Integer)
    Date_164 = db.Column(db.String(25))
    Rate_164 = db.Column(db.Integer)
    Date_165 = db.Column(db.String(25))
    Rate_165 = db.Column(db.Integer)
    Date_166 = db.Column(db.String(25))
    Rate_166 = db.Column(db.Integer)
    Date_167 = db.Column(db.String(25))
    Rate_167 = db.Column(db.Integer)
    Date_168 = db.Column(db.String(25))
    Rate_168 = db.Column(db.Integer)
    Date_169 = db.Column(db.String(25))
    Rate_179 = db.Column(db.Integer)
    Date_170 = db.Column(db.String(25))
    Rate_170 = db.Column(db.Integer)
    Date_171 = db.Column(db.String(25))
    Rate_171 = db.Column(db.Integer)
    Date_172 = db.Column(db.String(25))
    Rate_172 = db.Column(db.Integer)
    Date_173 = db.Column(db.String(25))
    Rate_173 = db.Column(db.Integer)
    Date_174 = db.Column(db.String(25))
    Rate_174 = db.Column(db.Integer)
    Date_175 = db.Column(db.String(25))
    Rate_175 = db.Column(db.Integer)
    Date_176 = db.Column(db.String(25))
    Rate_176 = db.Column(db.Integer)
    Date_177 = db.Column(db.String(25))
    Rate_177 = db.Column(db.Integer)
    Date_178 = db.Column(db.String(25))
    Rate_178 = db.Column(db.Integer)
    Date_179 = db.Column(db.String(25))
    Rate_179 = db.Column(db.Integer)
    Date_180 = db.Column(db.String(25))
    Rate_180 = db.Column(db.Integer)
    Date_181 = db.Column(db.String(25))
    Rate_181 = db.Column(db.Integer)
    Date_182 = db.Column(db.String(25))
    Rate_182 = db.Column(db.Integer)
    Date_183 = db.Column(db.String(25))
    Rate_183 = db.Column(db.Integer)
    Date_184 = db.Column(db.String(25))
    Rate_184 = db.Column(db.Integer)
    Date_185 = db.Column(db.String(25))
    Rate_185 = db.Column(db.Integer)
    Date_186 = db.Column(db.String(25))
    Rate_186 = db.Column(db.Integer)
    Date_187 = db.Column(db.String(25))
    Rate_187 = db.Column(db.Integer)
    Date_188 = db.Column(db.String(25))
    Rate_188 = db.Column(db.Integer)
    Date_189 = db.Column(db.String(25))
    Rate_189 = db.Column(db.Integer)
    Date_180 = db.Column(db.String(25))
    Rate_180 = db.Column(db.Integer)
    Date_181 = db.Column(db.String(25))
    Rate_181 = db.Column(db.Integer)
    Date_182 = db.Column(db.String(25))
    Rate_182 = db.Column(db.Integer)
    Date_183 = db.Column(db.String(25))
    Rate_183 = db.Column(db.Integer)
    Date_184 = db.Column(db.String(25))
    Rate_184 = db.Column(db.Integer)
    Date_185 = db.Column(db.String(25))
    Rate_185 = db.Column(db.Integer)
    Date_186 = db.Column(db.String(25))
    Rate_186 = db.Column(db.Integer)
    Date_187 = db.Column(db.String(25))
    Rate_187 = db.Column(db.Integer)
    Date_188 = db.Column(db.String(25))
    Rate_188 = db.Column(db.Integer)
    Date_189 = db.Column(db.String(25))
    Rate_189 = db.Column(db.Integer)
    Date_190 = db.Column(db.String(25))
    Rate_190 = db.Column(db.Integer)
    Date_191 = db.Column(db.String(25))
    Rate_191 = db.Column(db.Integer)
    Date_192 = db.Column(db.String(25))
    Rate_192 = db.Column(db.Integer)
    Date_193 = db.Column(db.String(25))
    Rate_193 = db.Column(db.Integer)
    Date_194 = db.Column(db.String(25))
    Rate_194 = db.Column(db.Integer)
    Date_195 = db.Column(db.String(25))
    Rate_195 = db.Column(db.Integer)
    Date_196 = db.Column(db.String(25))
    Rate_196 = db.Column(db.Integer)
    Date_197 = db.Column(db.String(25))
    Rate_197 = db.Column(db.Integer)
    Date_198 = db.Column(db.String(25))
    Rate_198 = db.Column(db.Integer)
    Date_199 = db.Column(db.String(25))
    Rate_199 = db.Column(db.Integer)
    Date_200 = db.Column(db.String(25))
    Rate_200 = db.Column(db.Integer)
    Date_201 = db.Column(db.String(25))
    Rate_201 = db.Column(db.Integer)
    Date_202 = db.Column(db.String(25))
    Rate_202 = db.Column(db.Integer)
    Date_203 = db.Column(db.String(25))
    Rate_203 = db.Column(db.Integer)
    Date_204 = db.Column(db.String(25))
    Rate_204 = db.Column(db.Integer)
    Date_205 = db.Column(db.String(25))
    Rate_205 = db.Column(db.Integer)
    Date_206 = db.Column(db.String(25))
    Rate_206 = db.Column(db.Integer)
    Date_207 = db.Column(db.String(25))
    Rate_207 = db.Column(db.Integer)
    Date_208 = db.Column(db.String(25))
    Rate_208 = db.Column(db.Integer)
    Date_209 = db.Column(db.String(25))
    Rate_209 = db.Column(db.Integer)
    Date_210 = db.Column(db.String(25))
    Rate_210 = db.Column(db.Integer)

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
    results = db.session.query(GoogleData.Category, GoogleData.Tag, GoogleData.Date_100, GoogleData.Rate_100, GoogleData.Date_101, GoogleData.Rate_101, GoogleData.Date_102, GoogleData.Rate_102, GoogleData.Date_103, GoogleData.Rate_103, GoogleData.Date_104, GoogleData.Rate_104, GoogleData.Date_105, GoogleData.Rate_105, GoogleData.Date_106, GoogleData.Rate_106, GoogleData.Date_107, GoogleData.Rate_107, GoogleData.Date_108, GoogleData.Rate_108, GoogleData.Date_109, GoogleData.Rate_109, GoogleData.Date_110, GoogleData.Rate_110, GoogleData.Date_111, GoogleData.Rate_111, GoogleData.Date_112, GoogleData.Rate_112, GoogleData.Date_113, GoogleData.Rate_113, GoogleData.Date_114, GoogleData.Rate_114, GoogleData.Date_115, GoogleData.Rate_115, GoogleData.Date_116, GoogleData.Rate_116, GoogleData.Date_117, GoogleData.Rate_117, GoogleData.Date_118, GoogleData.Rate_118, GoogleData.Date_119, GoogleData.Rate_119, GoogleData.Date_120, GoogleData.Rate_120, GoogleData.Date_121, GoogleData.Rate_121, GoogleData.Date_122, GoogleData.Rate_122, GoogleData.Date_123, GoogleData.Rate_123, GoogleData.Date_124, GoogleData.Rate_124, GoogleData.Date_125, GoogleData.Rate_125, GoogleData.Date_126, GoogleData.Rate_126, GoogleData.Date_127, GoogleData.Rate_127, GoogleData.Date_128, GoogleData.Rate_128, GoogleData.Date_129, GoogleData.Rate_129, GoogleData.Date_130, GoogleData.Rate_130, GoogleData.Date_131, GoogleData.Rate_131, GoogleData.Date_132, GoogleData.Rate_132, GoogleData.Date_133, GoogleData.Rate_133, GoogleData.Date_134, GoogleData.Rate_134, GoogleData.Date_135, GoogleData.Rate_135, GoogleData.Date_136, GoogleData.Rate_136, GoogleData.Date_137, GoogleData.Rate_137, GoogleData.Date_138, GoogleData.Rate_138, GoogleData.Date_139, GoogleData.Rate_139, GoogleData.Date_140, GoogleData.Rate_140, GoogleData.Date_141, GoogleData.Rate_141, GoogleData.Date_142, GoogleData.Rate_142, GoogleData.Date_143, GoogleData.Rate_143, GoogleData.Date_144, GoogleData.Rate_144, GoogleData.Date_145, GoogleData.Rate_145, GoogleData.Date_146, GoogleData.Rate_146, GoogleData.Date_147, GoogleData.Rate_147, GoogleData.Date_148, GoogleData.Rate_148, GoogleData.Date_149, GoogleData.Rate_149, GoogleData.Date_150, GoogleData.Rate_150, GoogleData.Date_151, GoogleData.Rate_151, GoogleData.Date_152, GoogleData.Rate_152, GoogleData.Date_153, GoogleData.Rate_153, GoogleData.Date_154, GoogleData.Rate_154, GoogleData.Date_155, GoogleData.Rate_155, GoogleData.Date_156, GoogleData.Rate_156, GoogleData.Date_157, GoogleData.Rate_157, GoogleData.Date_158, GoogleData.Rate_158, GoogleData.Date_159, GoogleData.Rate_159, GoogleData.Date_160, GoogleData.Rate_160, GoogleData.Date_161, GoogleData.Rate_161, GoogleData.Date_162, GoogleData.Rate_162, GoogleData.Date_163, GoogleData.Rate_163, GoogleData.Date_164, GoogleData.Rate_164, GoogleData.Date_165, GoogleData.Rate_165, GoogleData.Date_166, GoogleData.Rate_166, GoogleData.Date_167, GoogleData.Rate_167, GoogleData.Date_168, GoogleData.Rate_168, GoogleData.Date_169, GoogleData.Rate_179, GoogleData.Date_170, GoogleData.Rate_170, GoogleData.Date_171, GoogleData.Rate_171, GoogleData.Date_172, GoogleData.Rate_172, GoogleData.Date_173, GoogleData.Rate_173, GoogleData.Date_174, GoogleData.Rate_174, GoogleData.Date_175, GoogleData.Rate_175, GoogleData.Date_176, GoogleData.Rate_176, GoogleData.Date_177, GoogleData.Rate_177, GoogleData.Date_178, GoogleData.Rate_178, GoogleData.Date_179, GoogleData.Rate_179, GoogleData.Date_180, GoogleData.Rate_180, GoogleData.Date_181, GoogleData.Rate_181, GoogleData.Date_182, GoogleData.Rate_182, GoogleData.Date_183, GoogleData.Rate_183, GoogleData.Date_184, GoogleData.Rate_184, GoogleData.Date_185, GoogleData.Rate_185, GoogleData.Date_186, GoogleData.Rate_186, GoogleData.Date_187, GoogleData.Rate_187, GoogleData.Date_188, GoogleData.Rate_188, GoogleData.Date_189, GoogleData.Rate_189, GoogleData.Date_180, GoogleData.Rate_180, GoogleData.Date_181, GoogleData.Rate_181, GoogleData.Date_182, GoogleData.Rate_182, GoogleData.Date_183, GoogleData.Rate_183, GoogleData.Date_184, GoogleData.Rate_184, GoogleData.Date_185, GoogleData.Rate_185, GoogleData.Date_186, GoogleData.Rate_186, GoogleData.Date_187, GoogleData.Rate_187, GoogleData.Date_188, GoogleData.Rate_188, GoogleData.Date_189, GoogleData.Rate_189, GoogleData.Date_190, GoogleData.Rate_190, GoogleData.Date_191, GoogleData.Rate_191, GoogleData.Date_192, GoogleData.Rate_192, GoogleData.Date_193, GoogleData.Rate_193, GoogleData.Date_194, GoogleData.Rate_194, GoogleData.Date_195, GoogleData.Rate_195, GoogleData.Date_196, GoogleData.Rate_196, GoogleData.Date_197, GoogleData.Rate_197, GoogleData.Date_198, GoogleData.Rate_198, GoogleData.Date_199, GoogleData.Rate_199, GoogleData.Date_200, GoogleData.Rate_200, GoogleData.Date_201, GoogleData.Rate_201, GoogleData.Date_202, GoogleData.Rate_202, GoogleData.Date_203, GoogleData.Rate_203, GoogleData.Date_204, GoogleData.Rate_204, GoogleData.Date_205, GoogleData.Rate_205, GoogleData.Date_206, GoogleData.Rate_206, GoogleData.Date_207, GoogleData.Rate_207, GoogleData.Date_208, GoogleData.Rate_208, GoogleData.Date_209, GoogleData.Rate_209, GoogleData.Date_210, GoogleData.Rate_210)
    db.session.close()

    # Results of the query
    google_interest = []
    for Category, Tag, Busiest_date, Date_100 ,Rate_100 ,Date_101 ,Rate_101 ,Date_102 ,Rate_102 ,Date_103 ,Rate_103 ,Date_104 ,Rate_104 ,Date_105 ,Rate_105 ,Date_106 ,Rate_106 ,Date_107 ,Rate_107 ,Date_108 ,Rate_108 ,Date_109 ,Rate_109 ,Date_110 ,Rate_110 ,Date_111 ,Rate_111 ,Date_112 ,Rate_112 ,Date_113 ,Rate_113 ,Date_114 ,Rate_114 ,Date_115 ,Rate_115 ,Date_116 ,Rate_116 ,Date_117 ,Rate_117 ,Date_118 ,Rate_118 ,Date_119 ,Rate_119 ,Date_120 ,Rate_120 ,Date_121 ,Rate_121 ,Date_122 ,Rate_122 ,Date_123 ,Rate_123 ,Date_124 ,Rate_124 ,Date_125 ,Rate_125 ,Date_126 ,Rate_126 ,Date_127 ,Rate_127 ,Date_128 ,Rate_128 ,Date_129 ,Rate_129 ,Date_130 ,Rate_130 ,Date_131 ,Rate_131 ,Date_132 ,Rate_132 ,Date_133 ,Rate_133 ,Date_134 ,Rate_134 ,Date_135 ,Rate_135 ,Date_136 ,Rate_136 ,Date_137 ,Rate_137 ,Date_138 ,Rate_138 ,Date_139 ,Rate_139 ,Date_140 ,Rate_140 ,Date_141 ,Rate_141 ,Date_142 ,Rate_142 ,Date_143 ,Rate_143 ,Date_144 ,Rate_144 ,Date_145 ,Rate_145 ,Date_146 ,Rate_146 ,Date_147 ,Rate_147 ,Date_148 ,Rate_148 ,Date_149 ,Rate_149 ,Date_150 ,Rate_150 ,Date_151 ,Rate_151 ,Date_152 ,Rate_152 ,Date_153 ,Rate_153 ,Date_154 ,Rate_154 ,Date_155 ,Rate_155 ,Date_156 ,Rate_156 ,Date_157 ,Rate_157 ,Date_158 ,Rate_158 ,Date_159 ,Rate_159 ,Date_160 ,Rate_160 ,Date_161 ,Rate_161 ,Date_162 ,Rate_162 ,Date_163 ,Rate_163 ,Date_164 ,Rate_164 ,Date_165 ,Rate_165 ,Date_166 ,Rate_166 ,Date_167 ,Rate_167 ,Date_168 ,Rate_168 ,Date_169 ,Rate_179 ,Date_170 ,Rate_170 ,Date_171 ,Rate_171 ,Date_172 ,Rate_172 ,Date_173 ,Rate_173 ,Date_174 ,Rate_174 ,Date_175 ,Rate_175 ,Date_176 ,Rate_176 ,Date_177 ,Rate_177 ,Date_178 ,Rate_178 ,Date_179 ,Rate_179 ,Date_180 ,Rate_180 ,Date_181 ,Rate_181 ,Date_182 ,Rate_182 ,Date_183 ,Rate_183 ,Date_184 ,Rate_184 ,Date_185 ,Rate_185 ,Date_186 ,Rate_186 ,Date_187 ,Rate_187 ,Date_188 ,Rate_188 ,Date_189 ,Rate_189 ,Date_180 ,Rate_180 ,Date_181 ,Rate_181 ,Date_182 ,Rate_182 ,Date_183 ,Rate_183 ,Date_184 ,Rate_184 ,Date_185 ,Rate_185 ,Date_186 ,Rate_186 ,Date_187 ,Rate_187 ,Date_188 ,Rate_188 ,Date_189 ,Rate_189 ,Date_190 ,Rate_190 ,Date_191 ,Rate_191 ,Date_192 ,Rate_192 ,Date_193 ,Rate_193 ,Date_194 ,Rate_194 ,Date_195 ,Rate_195 ,Date_196 ,Rate_196 ,Date_197 ,Rate_197 ,Date_198 ,Rate_198 ,Date_199 ,Rate_199 ,Date_200 ,Rate_200 ,Date_201 ,Rate_201 ,Date_202 ,Rate_202 ,Date_203 ,Rate_203 ,Date_204 ,Rate_204 ,Date_205 ,Rate_205 ,Date_206 ,Rate_206 ,Date_207 ,Rate_207 ,Date_208 ,Rate_208 ,Date_209 ,Rate_209 ,Date_210 ,Rate_210 in results:
        each_interest = {}
        each_interest['Category'] = Category
        each_interest['Tag'] = Tag
        each_interest['Busiest_date'] = Busiest_date
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
        each_interest['Date_118'] = Date_118
        each_interest['Rate_118'] = Rate_118
        each_interest['Date_119'] = Date_119
        each_interest['Rate_119'] = Rate_119
        each_interest['Date_120'] = Date_120
        each_interest['Rate_120'] = Rate_120
        each_interest['Date_121'] = Date_121
        each_interest['Rate_121'] = Rate_121
        each_interest['Date_122'] = Date_122
        each_interest['Rate_122'] = Rate_122
        each_interest['Date_123'] = Date_123
        each_interest['Rate_123'] = Rate_123
        each_interest['Date_124'] = Date_124
        each_interest['Rate_124'] = Rate_124
        each_interest['Date_125'] = Date_125
        each_interest['Rate_125'] = Rate_125
        each_interest['Date_126'] = Date_126
        each_interest['Rate_126'] = Rate_126
        each_interest['Date_127'] = Date_127
        each_interest['Rate_127'] = Rate_127
        each_interest['Date_128'] = Date_128
        each_interest['Rate_128'] = Rate_128
        each_interest['Date_129'] = Date_129
        each_interest['Rate_129'] = Rate_129
        each_interest['Date_130'] = Date_130
        each_interest['Rate_130'] = Rate_130
        each_interest['Date_131'] = Date_131
        each_interest['Rate_131'] = Rate_131
        each_interest['Date_132'] = Date_132
        each_interest['Rate_132'] = Rate_132
        each_interest['Date_133'] = Date_133
        each_interest['Rate_133'] = Rate_133
        each_interest['Date_134'] = Date_134
        each_interest['Rate_134'] = Rate_134
        each_interest['Date_135'] = Date_135
        each_interest['Rate_135'] = Rate_135
        each_interest['Date_136'] = Date_136
        each_interest['Rate_136'] = Rate_136
        each_interest['Date_137'] = Date_137
        each_interest['Rate_137'] = Rate_137
        each_interest['Date_138'] = Date_138
        each_interest['Rate_138'] = Rate_138
        each_interest['Date_139'] = Date_139
        each_interest['Rate_139'] = Rate_139
        each_interest['Date_140'] = Date_140
        each_interest['Rate_140'] = Rate_140
        each_interest['Date_141'] = Date_141
        each_interest['Rate_141'] = Rate_141
        each_interest['Date_142'] = Date_142
        each_interest['Rate_142'] = Rate_142
        each_interest['Date_143'] = Date_143
        each_interest['Rate_143'] = Rate_143
        each_interest['Date_144'] = Date_144
        each_interest['Rate_144'] = Rate_144
        each_interest['Date_145'] = Date_145
        each_interest['Rate_145'] = Rate_145
        each_interest['Date_146'] = Date_146
        each_interest['Rate_146'] = Rate_146
        each_interest['Date_147'] = Date_147
        each_interest['Rate_147'] = Rate_147
        each_interest['Date_148'] = Date_148
        each_interest['Rate_148'] = Rate_148
        each_interest['Date_149'] = Date_149
        each_interest['Rate_149'] = Rate_149
        each_interest['Date_150'] = Date_150
        each_interest['Rate_150'] = Rate_150
        each_interest['Date_151'] = Date_151
        each_interest['Rate_151'] = Rate_151
        each_interest['Date_152'] = Date_152
        each_interest['Rate_152'] = Rate_152
        each_interest['Date_153'] = Date_153
        each_interest['Rate_153'] = Rate_153
        each_interest['Date_154'] = Date_154
        each_interest['Rate_154'] = Rate_154
        each_interest['Date_155'] = Date_155
        each_interest['Rate_155'] = Rate_155
        each_interest['Date_156'] = Date_156
        each_interest['Rate_156'] = Rate_156
        each_interest['Date_157'] = Date_157
        each_interest['Rate_157'] = Rate_157
        each_interest['Date_158'] = Date_158
        each_interest['Rate_158'] = Rate_158
        each_interest['Date_159'] = Date_159
        each_interest['Rate_159'] = Rate_159
        each_interest['Date_160'] = Date_160
        each_interest['Rate_160'] = Rate_160
        each_interest['Date_161'] = Date_161
        each_interest['Rate_161'] = Rate_161
        each_interest['Date_162'] = Date_162
        each_interest['Rate_162'] = Rate_162
        each_interest['Date_163'] = Date_163
        each_interest['Rate_163'] = Rate_163
        each_interest['Date_164'] = Date_164
        each_interest['Rate_164'] = Rate_164
        each_interest['Date_165'] = Date_165
        each_interest['Rate_165'] = Rate_165
        each_interest['Date_166'] = Date_166
        each_interest['Rate_166'] = Rate_166
        each_interest['Date_167'] = Date_167
        each_interest['Rate_167'] = Rate_167
        each_interest['Date_168'] = Date_168
        each_interest['Rate_168'] = Rate_168
        each_interest['Date_169'] = Date_169
        each_interest['Rate_179'] = Rate_179
        each_interest['Date_170'] = Date_170
        each_interest['Rate_170'] = Rate_170
        each_interest['Date_171'] = Date_171
        each_interest['Rate_171'] = Rate_171
        each_interest['Date_172'] = Date_172
        each_interest['Rate_172'] = Rate_172
        each_interest['Date_173'] = Date_173
        each_interest['Rate_173'] = Rate_173
        each_interest['Date_174'] = Date_174
        each_interest['Rate_174'] = Rate_174
        each_interest['Date_175'] = Date_175
        each_interest['Rate_175'] = Rate_175
        each_interest['Date_176'] = Date_176
        each_interest['Rate_176'] = Rate_176
        each_interest['Date_177'] = Date_177
        each_interest['Rate_177'] = Rate_177
        each_interest['Date_178'] = Date_178
        each_interest['Rate_178'] = Rate_178
        each_interest['Date_179'] = Date_179
        each_interest['Rate_179'] = Rate_179
        each_interest['Date_180'] = Date_180
        each_interest['Rate_180'] = Rate_180
        each_interest['Date_181'] = Date_181
        each_interest['Rate_181'] = Rate_181
        each_interest['Date_182'] = Date_182
        each_interest['Rate_182'] = Rate_182
        each_interest['Date_183'] = Date_183
        each_interest['Rate_183'] = Rate_183
        each_interest['Date_184'] = Date_184
        each_interest['Rate_184'] = Rate_184
        each_interest['Date_185'] = Date_185
        each_interest['Rate_185'] = Rate_185
        each_interest['Date_186'] = Date_186
        each_interest['Rate_186'] = Rate_186
        each_interest['Date_187'] = Date_187
        each_interest['Rate_187'] = Rate_187
        each_interest['Date_188'] = Date_188
        each_interest['Rate_188'] = Rate_188
        each_interest['Date_189'] = Date_189
        each_interest['Rate_189'] = Rate_189
        each_interest['Date_180'] = Date_180
        each_interest['Rate_180'] = Rate_180
        each_interest['Date_181'] = Date_181
        each_interest['Rate_181'] = Rate_181
        each_interest['Date_182'] = Date_182
        each_interest['Rate_182'] = Rate_182
        each_interest['Date_183'] = Date_183
        each_interest['Rate_183'] = Rate_183
        each_interest['Date_184'] = Date_184
        each_interest['Rate_184'] = Rate_184
        each_interest['Date_185'] = Date_185
        each_interest['Rate_185'] = Rate_185
        each_interest['Date_186'] = Date_186
        each_interest['Rate_186'] = Rate_186
        each_interest['Date_187'] = Date_187
        each_interest['Rate_187'] = Rate_187
        each_interest['Date_188'] = Date_188
        each_interest['Rate_188'] = Rate_188
        each_interest['Date_189'] = Date_189
        each_interest['Rate_189'] = Rate_189
        each_interest['Date_190'] = Date_190
        each_interest['Rate_190'] = Rate_190
        each_interest['Date_191'] = Date_191
        each_interest['Rate_191'] = Rate_191
        each_interest['Date_192'] = Date_192
        each_interest['Rate_192'] = Rate_192
        each_interest['Date_193'] = Date_193
        each_interest['Rate_193'] = Rate_193
        each_interest['Date_194'] = Date_194
        each_interest['Rate_194'] = Rate_194
        each_interest['Date_195'] = Date_195
        each_interest['Rate_195'] = Rate_195
        each_interest['Date_196'] = Date_196
        each_interest['Rate_196'] = Rate_196
        each_interest['Date_197'] = Date_197
        each_interest['Rate_197'] = Rate_197
        each_interest['Date_198'] = Date_198
        each_interest['Rate_198'] = Rate_198
        each_interest['Date_199'] = Date_199
        each_interest['Rate_199'] = Rate_199
        each_interest['Date_200'] = Date_200
        each_interest['Rate_200'] = Rate_200
        each_interest['Date_201'] = Date_201
        each_interest['Rate_201'] = Rate_201
        each_interest['Date_202'] = Date_202
        each_interest['Rate_202'] = Rate_202
        each_interest['Date_203'] = Date_203
        each_interest['Rate_203'] = Rate_203
        each_interest['Date_204'] = Date_204
        each_interest['Rate_204'] = Rate_204
        each_interest['Date_205'] = Date_205
        each_interest['Rate_205'] = Rate_205
        each_interest['Date_206'] = Date_206
        each_interest['Rate_206'] = Rate_206
        each_interest['Date_207'] = Date_207
        each_interest['Rate_207'] = Rate_207
        each_interest['Date_208'] = Date_208
        each_interest['Rate_208'] = Rate_208
        each_interest['Date_209'] = Date_209
        each_interest['Rate_209'] = Rate_209
        each_interest['Date_210'] = Date_210
        each_interest['Rate_210'] = Rate_210
        google_interest.append(each_interest)


    return jsonify(google_interest)


if __name__ == "__main__":
    app.run(debug=True)


