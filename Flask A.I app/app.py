import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,flash,session,flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json','r') as file:
    parameter=json.load(file)['params']

local_server=parameter['local_server']

app = Flask(__name__)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']

db = SQLAlchemy(app)

#class of registartion of users in database SignUp
class Registeredusers(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cellNo = db.Column(db.String(50), primary_key=False)
    userPassword = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120),nullable=False)

#class of contact us data in database index


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


#code for signup and send user data into the register users database table
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        fullName = request.form.get('username')
        email = request.form.get('email')
        cellNo = request.form.get('cellNo')
        userPassword = request.form.get('userPassword')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        entry = Registeredusers(fullName=fullName, email=email,cellNo=cellNo,userPassword=userPassword,dob=dob,gender=gender)
        db.session.add(entry)
        db.session.commit()
    return render_template('signup.html')
#Code for Login Authenticating

@app.route('/authenticating',methods=['GET','POST'])
def authenticate():
    getedemail = request.form.get('email')
    getedpass = request.form.get('password')
    rows = Registeredusers.query.filter_by(email=getedemail, userPassword=getedpass).all()
    if rows:
        session['logged_in'] == True
        return render_template('dashboardLayout.html',rows=rows)
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
