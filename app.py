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

def connect_db():
    connection = sql.connect(app.database)
    connection.row_factory = sql.Row 
    return connection

def getCursor():
    return connect_db().cursor()

@app.route('/')
def index():
    cur = getCursor()
    cur.execute("select mission from launches")
    rows = cur.fetchall()
    if len(rows)>0:
        launch = rows[0]
    mission = launch['mission']
    return render_template('home.html', mission=mission)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
