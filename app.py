from flask import Flask, render_template, flash, redirect, url_for, session, logging, g, request
from data import Articles
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.debug = True

#SQL
app.database = "myflaskapp.db"
app.secret_key='secret123'


Articles = Articles()
def connect_db():
    return sql.connect(app.database)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html',articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor
        g.db = connect_db()

        #insert values
        g.db.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)", (name, email, username, password))

        #commit and close
        g.db.commit()
        g.db.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        
        #Create cursor
        con = sql.connect("myflaskapp.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users WHERE username = ?", [username])
        rows = cur.fetchall(); 

        if len(rows) > 0:
            # Get stored hash
            data = rows[0]
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid login"
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = "Username not found"
            return render_template('login.html',error=error)

    return render_template('login.html')

# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
    
# User Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# user Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('/dashboard.html')


if __name__ == '__main__':
    app.run()
