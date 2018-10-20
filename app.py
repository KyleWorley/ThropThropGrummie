from flask import Flask, render_template, flash, redirect, url_for, session, logging, g, request
from data import Articles
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.debug = True

#SQL
app.database = "spaceapps.db"
app.secret_key='#SpaceAppsHSV'

class launch:
    def __init__(self, date, time, country, state, location,
            Manufacturer, model, mission, Description, link, image):
        self.date = date
        self.time = time
        self.country = country
        self.state = state
        self.location = location
        self.Manufacturer = Manufacturer
        self.model = model
        self.mission = mission
        self.Description = Description
        self.link = link
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
            l = launch(row['date'], row['time'], row['country'],
                    row['state'],row['location'], row['Manufacturer'],
                    row['model'], row['mission'], row['Description'],
                    row['link'], row['image'])
            app.logger.info(l.image)
            launches.append(l)

    return render_template('home.html', launches=launches)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
