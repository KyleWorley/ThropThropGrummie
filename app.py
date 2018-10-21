from flask import Flask, render_template, flash, redirect, url_for, session, logging, g, request
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from requests import get
from requests_oauthlib import OAuth1Session
import json
import yaml

app = Flask(__name__)
app.debug = True

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

#SQL
app.database = cfg['sqlite3']['database']
app.secret_key = cfg['sqlite3']['secret-key']

class launch:
    def __init__(self, date, time, location,
            vehicle, mission, description, articles, image):
        self.date = date
        self.time = time
        self.location = location
        self.vehicle = vehicle
        self.mission = mission
        self.description = description
        self.articles = articles 
        self.image = image

def connect_db():
    connection = sql.connect(app.database)
    connection.row_factory = sql.Row 
    return connection 
def getCursor():
    return connect_db().cursor()

@app.route('/')
def index():
    cur = getCursor()
    cur.execute("select * from launches")
    rows = cur.fetchall()
    launches = []
    if len(rows)>0:
        for i in range(0,len(rows)):
            row = rows[i]
            l = launch(row['date'], row['time'],
                    row['location'], row['vehicle'],
                    row['mission'], row['description'],
                    row['articles'], row['image'])
            app.logger.info(l.image)
            launches.append(l)
    cur.close()

    return render_template('home.html', launches=launches)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/launch/<string:mission>/')
def launchpage(mission):
    cur = getCursor()
    cur.execute("select * from launches where mission = ?", [mission])
    rows = cur.fetchall()
    l = rows[0]
    hashtag = l['mission'] + '-' + l['vehicle']
    hashtag = hashtag.replace(' ', '')
    app.logger.info(hashtag)
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23' + hashtag + '&result_type=recent'
    images = get(url)
    session = OAuth1Session(cfg['twitter']['api-key'],
                    client_secret=cfg['twitter']['secret'])
    r = session.get(url)
    #app.logger.info(r.content)
    responseString = r.content.decode('utf-8')
    responseJson = json.loads(responseString)
    userImages = []
    statuses = responseJson["statuses"]
    for statusDict in statuses:
        entities = statusDict['entities']
        app.logger.info(entities)
        media = entities['media'][0]
        app.logger.info(media['media_url_https'])
        userImages.append(media['media_url_https'])
    date = str(l['date'])
    app.logger.info(date)

    date = date[4:6] + '/' + date[6:8] + '/' + date[0:4]
    cur.close()
    return render_template('launch.html', launch=l, date = date, hashtag = hashtag, images=userImages)

if __name__ == '__main__':
    app.run()



