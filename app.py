from flask import Flask, render_template, flash, redirect, url_for, session, logging, g, request
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from requests import get
from requests_oauthlib import OAuth1Session
#from SpaceAppsUtil.py import *

app = Flask(__name__)
app.debug = True

#SQL
app.database = "spaceapps.db"
app.secret_key='#SpaceAppsHSV'

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
    hashtag = l['mission']
    app.logger.info(hashtag)
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23' + hashtag + '&result_type=recent'
    images = get(url)
    session = OAuth1Session('KbFIpnP6oaZkSka4wSRqEk8Qz',
                    client_secret='7R2Dcb1BZod4aXbyzukOJYJF6lMR0ExOe5Fk7me3jCWhgf3Iz3')
    r = session.get(url)
    app.logger.info(r.content)
    app.logger.info(images.status_code)
    date = str(l['date'])
    app.logger.info(date)
    #dateWords = dateToWords(int(date))# making date into words
    date = date[4:6] + '/' + date[6:8] + '/' + date[0:4]
    cur.close()
    return render_template('launch.html', launch=l, date = date)

def dateToWords(dateNum):
    # get day
    day = dateNum % 100
    dateNum = dateNum / 100
    # get month
    m = dateNum %100
    dateNum = dateNum/100
    if m == 1:
        month = "January"
    elif m == 2:
        month = "February"
    elif m == 3:
        month = "March"
    elif m == 4:
        month = "April"
    elif m == 5:
        month = "May"
    elif m == 6:
        month = "June"
    elif m == 7:
        month = "July"
    elif m == 8:
        month = "August"
    elif m == 9:
        month = "September"
    elif m == 10:
        month = "October"
    elif m == 11:
        month = "November"
    elif m == 12:
        month = "December"
    else:
        month = m
    # get year
    year = dateNum
    dateWords = month + day + year
    return dateWords


if __name__ == '__main__':
    app.run()



