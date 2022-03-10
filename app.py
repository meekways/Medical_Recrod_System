from crypt import methods
import email
from unicodedata import name
from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import re
from random import randint


app = Flask(__name__)


#Database configuration below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'winner2244'
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)

@app.route("/", methods=["POST"])
def index():
    return render_template('index.html')



@app.route("/registration/", methods=["GET", "POST"])
def registration():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']
        cpassword = userDetails['cpassword']
        user_type = userDetails['user_type']

        random_int = randint(1000, 9999)
        patient_id = f"JLS-{random_int}"
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE (username, password) VALUES(%s, %s)', ('username', 'password'))
        account = cursor.fetchone()
        if account:
            msg = 'account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@])+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (username, email, password, user_type))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return redirect('login.html')
    return render_template("registration.html", msg = msg)


@app.route("/login/", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'role' in request.form:
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        user_type = userDetails['user_type']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users(username, password) VALUES(%s, %s)', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            session['user_type'] = account['user_type']
            msg = 'Logged in successfully !'

            if account['user_type'] == 'admin':
                return render_template('admin.html')
            elif account['user_type'] == 'record attendant':
                return render_template('record.html')
            elif account['user_type'] == 'consultant/doctor':
                return render_template('consultant.html')
            elif account['user_type'] == 'lab attendant':
                return render_template('lab.html')
            else:
                return redirect('index.html', msg = msg)
        else:
            msg = 'Incorrect name / password!'
            return render_template("login.html", msg = msg)
    return render_template('login.html')

@app.route("/admin/",  methods=["GET", "POST"])
def admin():
    return render_template('admin.html', name="admin")

@app.route("/consultant/",  methods=["GET", "POST"])
def consultant():
    return render_template('consultant.html', name="consultant")

@app.route("/record/", methods=["GET", "POST"])
def record():
    return render_template("record.html")

@app.route("/lab/",  methods=["GET", "POST"])
def lab():
    return render_template('lab.html', name="lab")
        

if __name__ == "__main__":
    app.run(debug=True)