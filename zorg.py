#postgresql might work
#discarded wtforms, which created the trouble
#features lost: password encryption, has to be changed everywhere
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import csv
import os
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app=Flask(__name__)

ENV = 'dev'

developer='Tarun'

if ENV=='dev':
    app.debug=True
    if developer=='Arjun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgre-arj4703@localhost/Zorg'
    elif developer=='Tarun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Tarun@postgresql@localhost/Zorg'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nodkzxyxsbqfdj:e12cbd58f24bb6ee6c9896c2731480a784a73b81fd860b2a245135b372c4f32@ec2-54-236-146-234.compute-1.amazonaws.com:5432/d2hmpp8n530vvp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

@app.route('/')
def home():
    return  render_template('index.html')

class RegisterMnmg(db.Model):
    __tablename__ = 'hospdetails'
    namehptl = db.Column(db.String(200))
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(20))
    pincode = db.Column(db.Integer)
    address = db.Column(db.Text())

    def __init__(self, namehptl, username, password, pincode, address):
        self.namehptl = namehptl
        self.username = username
        self.password = password
        self.pincode = pincode
        self.address = address
@app.route('/registermnmg', methods=['GET','POST'])
def registermnmg():
    if request.method == 'POST':
        namehptl = request.form['namehptl'] 
        username = request.form['username']
        password = request.form['password']
        pincode = request.form['pincode'] 
        address = request.form['address']

        if db.session.query(RegisterMnmg).filter(RegisterMnmg.username == username).count() == 0:
            data = RegisterMnmg(namehptl, username, password, pincode, address)
            db.session.add(data)
            db.session.commit()
            flash('you are now registered', 'success')
            return redirect(url_for('loginmanagement'))
        else:
            flash("Username already exists", 'danger')
    return render_template('remnmg.html')

class CustomerDet(db.Model):#changed the class name since it is getting confused between the class and the table name
    __tablename__ = 'custdetails'
    namecust = db.Column(db.String(200))
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(20))
    pincode = db.Column(db.Integer())
    address = db.Column(db.Text())
    gmail_id = db.Column(db.String(200))
    aadhar = db.Column(db.Integer, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    prevmedrcrds = db.Column(db.Text())

    def __init__(self, namecust, username, password, pincode, address, gmail_id, aadhar, age, gender, prevmedrcrds):
        self.namecust = namecust
        self.username = username
        self.password = password
        self.pincode = pincode
        self.address = address
        self.gmail_id = gmail_id
        self.aadhar = aadhar
        self.age = age
        self.gender = gender
        self.prevmedrcrds = prevmedrcrds

@app.route('/custdetails', methods=['GET','POST'])
def custdetails():
    if request.method == 'POST':
        namecust = request.form['namecust'] 
        username = request.form['username']
        password = request.form['password']
        gmail_id = request.form['gmail_id']
        address = ''
        pincode = 0
        aadhar = 0
        age = 0
        gender = ''
        prevmedrcrds = ''

        if db.session.query(custdetails).filter(custdetails.username == username).count() == 0:
            data = custdetails(namecust, username, password, pincode, address, gmail_id, aadhar, age, gender, prevmedrcrds)#needs all the columns to run without errors
            db.session.add(data)
            db.session.commit()
            flash('you are now registered', 'success')
            return redirect(url_for('logincustomer'))
        else:
            flash("Username already exists", 'danger')
    return render_template('recust.html')    

@app.route('/loginmanagement', methods=['GET','POST'])
def loginmanagement():
    if request.method == 'POST':
        usermnmg = request.form['username']
        password_candidate = request.form['password']
        user = db.session.query(RegisterMnmg).filter(RegisterMnmg.username == usermnmg).first()
        db.session.commit()
        if user is None:
            flash('No such username exists', 'danger')
            return render_template('lomnmg.html')
        else:
            if password_candidate == user.password:
                session['logged_in'] = True
                session['username'] = usermnmg
                session['name'] = user.namehptl
                flash('You are now logged in','success')
                return redirect(url_for('kindly'))
            else:
                flash('Incorrect password','danger')
                return render_template('lomnmg.html')
    else:
        return render_template('lomnmg.html')

@app.route('/logincustomer', methods=['GET','POST'])
def logincustomer():
    if request.method == 'POST':
        usercust = request.form['username']
        password_candidate = request.form['password']
        user = db.session.query(custdetails).filter(custdetails.username == usercust).first()
        db.session.commit()
        if user is None:
            flash('No such username exists', 'danger')
            return render_template('locust.html')
        else:
            if password_candidate == user.password:
                session['logged_in'] = True
                session['username'] = usercust
                session['name'] = user.namecust
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect password','danger')
                return render_template('locust.html')
    else:
        return render_template('locust.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORISED, Please Login','danger')
            return redirect(url_for('home'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET','POST'])
@is_logged_in
def dashboard():
    username = session['username']
    custdata = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()#111
    db.session.commit()
    if custdata.aadhar !=0 and custdata.age != 0 and custdata.gender != '' and custdata.prevmedrcrds != '' and custdata.address != '' and custdata.pincode != 0:
        return render_template('dashboard.html', profile = custdata.query.all())
    else:
        flash("Please fill these details","danger")
        return redirect(url_for('add_profile'))
    return render_template('dashboard.html')    

@app.route('/add_profile', methods=['GET','POST'])
@is_logged_in
def add_profile():
    username = session['username']
    if request.method =='POST':
        aadhar = request.form['aadhar']
        age = request.form['age']
        gender = request.form['gender']
        prevmedrcrds = request.form['prevmedrcrds']
        address = request.form['address']
        pincode = request.form['pincode']
        if db.session.query(custdetails).filter(custdetails.username == username).count() == 0:
            data = custdetails(name, aadhar, age, gender,prevmedrcrds, address, pincode)
            db.session.add(data)
            db.session.commit()
            flash('Profile Created', 'success')
            return redirect(url_for('loginmanagement'))
        else:
            return redirect(url_for('editprofile'))
    return render_template('add_profile.html')

@app.route('/editprofile', methods=['GET','POST'])
@is_logged_in
def editprofile():
    username = session['username']
    user = db.session.query(custdetails).filter(custdetails.username == username).first()
    db.session.commit()
    if request.method == 'POST':
        user.aadhar = request.form['aadhar']
        user.age = request.form['age']
        user.gender = request.form['gender']
        user.prevmedrcrds = request.form['prevmedrcrds']
        user.address = request.form['address']
        user.pincode = request.form['pincode']
        user.gmail_id = request.form['gmail_id']
        db.commit()
        flash('Profile Updated','success')
        return redirect(url_for('dashboard'))
    return render_template('editprofile.html')

class Orders(db.Model):
    __tablename__ = 'orders'
    hptl_username_in_vicinity = db.Column(db.String(200))
    username_cust = db.Column(db.String(200), primary_key=True)
    type = db.Column(db.String(50))
    address = db.Column(db.Text())
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    prevmedrcrds = db.Column(db.Text())
    result = db.Column(db.String(1))

    def __init__(self, hptl_username_in_vicinity, username_cust, type, address, age, gender, prevmedrcrds, result):
        self.hptl_username_in_vicinity = hptl_username_in_vicinity
        self.username_cust = username_cust
        self.type = type
        self.address = address
        self.namecust = namecust
        self.aadhar = aadhar 
        self.age = age
        self.gender = gender
        self.prevmedrcrds = prevmedrcrds
        self.result = result

@app.route('/accident')
@is_logged_in
def accident():
    username = session['username']
    pincode = session['pincode']
    list_of_hosp_to_send_message = []
    profile = db.session.query(custdetails).filter(custdetails.username == username).first()
    db.session.commit()
    if profile is not None:
        if db.session.query(Orders).filter(Orders.username == username).count() == 0:
            type='accident'
            for hospital in hospdetails:
                if hospital.pincode == pincode_cust:
                    list_of_hosp_to_send_message.append(hospital.username)
            #send to all hospitals at the same time
            for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.name, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                db.session.add(data)
                db.session.commit()
            return render_template('request_sent.html')
        else:
            flash('you have already sent a request, kindly wait till it is processed','danger')
            return render_template('request_sent.html')
    else:
        flash('please fill in your details so that we can send it to the hospitals','danger')
        return redirect(url_for('add_profile'))
    return render_template('request_sent.html')

@app.route('/heartattack')
@is_logged_in
def heartattack():
    username = session['username']
    pincode = session['pincode']
    list_of_hosp_to_send_message = []
    profile = db.session.query(custdetails).filter(custdetails.username == username).first()
    db.session.commit()
    if profile is not None:
        if db.session.query(Orders).filter(Orders.username == username).count() == 0:
            type='heart attack'
            for hospital in hospdetails:
                if hospital.pincode == pincode_cust:
                    list_of_hosp_to_send_message.append(hospital.username)
            #send to all hospitals at the same time
            for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.name, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                db.session.add(data)
                db.session.commit()
            return render_template('request_sent.html')
        else:
            flash('you have already sent a request, kindly wait till it is processed','danger')
            return render_template('request_sent.html')
    else:
        flash('please fill in your details so that we can send it to the hospitals','danger')
        return redirect(url_for('add_profile'))
    return render_template('request_sent.html')


@app.route('/otherailments')
@is_logged_in
def otherailments():
    username = session['username']
    pincode = session['pincode']
    list_of_hosp_to_send_message = []
    profile = db.session.query(custdetails).filter(custdetails.username == username).first()
    db.session.commit()
    if profile is not None:
        if db.session.query(Orders).filter(Orders.username == username).count() == 0:
            type='other ailments'
            for hospital in hospdetails:
                if hospital.pincode == pincode_cust:
                    list_of_hosp_to_send_message.append(hospital.username)
            #send to all hospitals at the same time
            for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.name, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                db.session.add(data)
                db.session.commit()
            return render_template('request_sent.html')
        else:
            flash('you have already sent a request, kindly wait till it is processed','danger')
            return render_template('request_sent.html')
    else:
        flash('please fill in your details so that we can send it to the hospitals','danger')
        return redirect(url_for('add_profile'))
    return render_template('request_sent.html')


class PastOrders(db.Model):
    __tablename__ = 'pastorders'
    number = db.Column(db.Integer, primary_key=True)
    name_of_hptl_accepting_responsibilty = db.Column(db.String(200))
    username_cust = db.Column(db.String(200))
    type = db.Column(db.String(50))
    address = db.Column(db.Text())
    namecust = db.Column(db.String(200))
    aadhar = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    prevmedrcrds = db.Column(db.Text())

    def __init__(self, number, name_of_hptl_accepting_responsibilty, username_cust, type, address, namecust, aadhar, age, gender, prevmedrcrds):
        self.number = number
        self.name_of_hptl_accepting_responsibilty = name_of_hptl_accepting_responsibilty
        self.username_cust = username_cust
        self.type = type
        self.address = address
        self.namecust = namecust
        self.aadhar = aadhar 
        self.age = age
        self.gender = gender
        self.prevmedrcrds = prevmedrcrds

@app.route('/dashboardmnmg')
@is_logged_in
def dashboardmnmg():
    username = session['username']
    profile = db.session.query(order).all()
    db.commit()
    if profile is not None:
        return render_template('dashboardmnmg.html', profile=profile)
    else:
        return redirect(url_for('dashboardmnmg.html'))
    return render_template('dashboardmnmg.html') 

class Result(db.Model):
    __tablename__ = 'result'
    name_of_hptl_result = db.Column(db.String(200))
    username_cust = db.Column(db.String(200), primary_key=True)
    acc_or_dec = db.Column(db.String(1))

    def __init__(self, name_of_hptl_result, username_cust, acc_or_dec):
        self.name_of_hptl_result = name_of_hptl_result
        self.username_cust = username_cust
        self.acc_or_dec = acc_or_dec

@app.route('/accepted/<username>')
@is_logged_in
def accepted(username):
    if db.session.query(Orders).filter(Orders.username_cust == username).count() == 1:
        acc_or_dec = "a"
        name_of_hptl_result = session['name']
        username_cust = username

        #send mail to that person!!!!! important
        user = db.session.query(custdetails).filter(custdetails.username == username).first()
        gmail_id = user.gmail_id
        #delete data from orders
        #add data to past orders
        flash('you have accepted to save '+username, 'success')
    return render_template('dashboardmnmg.html')

@app.route('/declined/<username>')
@is_logged_in
def declined(username):
    if db.session.query(Orders).filter(Orders.username_cust == username).count() == 1:
        acc_or_dec = "d"
        name_of_hptl_result = session['name']
        username_cust = username

        #send mail to that person!!!!! important
        user = db.session.query(custdetails).filter(custdetails.username == username).first()
        gmail_id = user.gmail_id
        #delete data from orders
        #add data to past orders
        flash('you have declined to save '+username, 'danger')
    return render_template('dashboardmnmg.html')

if __name__=='__main__':
    app.secret_key='secret123'
    app.run()

'''needed htmls
1)dashboardmnmg.html
2)not sure if we need accepted/declined.html
3)saved.html
4)not_saved.html
'''