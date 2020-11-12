from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt as sa
import csv
import os
import random
import math
from modules import *

app=Flask(__name__)

ENV = 'dev'

developer='Arjun'

if ENV=='dev':
    app.debug=True
    app.config['SECRET_KEY'] = 'awwfaw'
    if developer=='Arjun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgre-arj4703@localhost/Zorg'
    elif developer=='Tarun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Tarun@postgresql@localhost/Zorg'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxceiafawftfoj:be308eb925667514c2f0102ea54672bd5b11a3c6643062b2012dedc396304b36@ec2-54-237-155-151.compute-1.amazonaws.com:5432/d82ngqr88afvm9'
    app.config['SECRET_KEY'] = os.environ['secret']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method == "POST":
        mailid = request.form['mailid']
        feedback = request.form['feedback']
        try:
            emailsend(mailid, "Feedback Submitted:\n"+feedback)
            flash('Your response has been recorded','success')
            return redirect(url_for('home'))
        except:
            flash('Please enter all the details asked for','danger')
            return render_template('feedback.html')
        return render_template('feedback.html')
    return render_template('feedback.html')

@app.route('/footer',methods=['GET','POST'])
def footer():
    return render_template('Bootstrap Footer Template.html')
@app.route('/route', methods=['GET','POST'])
def route():
    return render_template('route.html')

@app.route('/google91184105f55d44d3')
def google91184105f55d44d3():
    return render_template('google91184105f55d44d3.html')

@app.route('/.well-known/pki-validation/22BF78F1880472211C2C4580C3EBCEF4.txt')
def ssl():
    return render_template('ssl.html')

def username_predict(u,t):
    c=True
    while c:
        if not db.session.query(t).filter(t.username == u).count() == 0:
            x=random.randint(0,6000)
            u+=str(x)
            s=". Try "+u
            c=False
    return s


class RegisterMnmg(db.Model):
    __tablename__ = 'hospdetails'
    namehptl = db.Column(db.String(200))
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(300))
    pincode = db.Column(db.String(10))
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
        password = sa.hash(request.form['password'])
        pincode = request.form['pincode'] 
        address = request.form['address']
        if db.session.query(RegisterMnmg).filter(RegisterMnmg.username == username).count() == 0:
            data = RegisterMnmg(namehptl, username, password, pincode, address)
            db.session.add(data)
            db.session.commit()
            flash('you are now registered', 'success')
            return redirect(url_for('loginmanagement'))
        else:
            flash("Username already exists"+username_predict(username, RegisterMnmg), 'danger')
    return render_template('remnmg.html')

class CustomerDet(db.Model):
    __tablename__ = 'custdetails'
    custid = db.Column(db.Integer, primary_key=True)
    namecust = db.Column(db.String(200))
    username = db.Column(db.String(200))
    password = db.Column(db.String(300))
    pincode = db.Column(db.String(10))
    address = db.Column(db.Text())
    gmail_id = db.Column(db.String(200))
    aadhar = db.Column(db.String(20))
    age = db.Column(db.String(5))
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
        password = sa.hash(request.form['password'])
        gmail_id = request.form['gmail_id']
        aadhar = request.form['aadhar']
        address = ''
        pincode = ''
        age = ''
        gender = ''
        prevmedrcrds = ''
        if db.session.query(CustomerDet).filter(CustomerDet.username == username).count() == 0:
            data = CustomerDet(namecust, username, password, pincode, address, gmail_id, aadhar, age, gender, prevmedrcrds)#needs all the columns to run without errors
            db.session.add(data)
            db.session.commit()
            flash('you are now registered', 'success')
            return redirect(url_for('logincustomer'))
        else:
            flash("Username already exists"+username_predict(username, CustomerDet), 'danger')
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
            if sa.verify(password_candidate, user.password):
                session['logged_in'] = True
                session['username'] = usermnmg
                session['name'] = user.namehptl
                session['type'] = 'H'
                session['pincode'] = user.pincode
                flash('You are now logged in','success')
                return redirect(url_for('dashboardmnmg'))
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
        user = db.session.query(CustomerDet).filter(CustomerDet.username == usercust).first()
        db.session.commit()
        if user is None:
            flash('No such username exists', 'danger')
            return render_template('locust.html')
        else:
            if sa.verify(password_candidate, user.password):
                session['logged_in'] = True
                session['username'] = usercust
                session['type'] = 'C'
                session['name'] = user.namecust
                session['pincode'] = user.pincode
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

@app.route('/dashboard', methods=['GET','POST'])
@is_logged_in
def dashboard():
    username = session['username']
    custdata = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    db.session.commit()
    if custdata.aadhar == '' or custdata.age == '' or custdata.gender == '' or custdata.prevmedrcrds == '' or custdata.address == '' or custdata.pincode == '':
        flash("Please fill these details","danger")
        return redirect(url_for('add_profile'))
    else:
        return render_template('dashboard.html', custdata = db.session.query(CustomerDet).filter(CustomerDet.username == username).all())
    return render_template('dashboard.html')  

@app.route('/add_profile', methods=['GET','POST'])
@is_logged_in
def add_profile():
    username = session['username']
    if request.method =='POST':
        age = request.form['age']
        gender = request.form['gender']
        prevmedrcrds = request.form['prevmedrcrds']
        address = request.form['address']
        pincode = request.form['pincode']
        if db.session.query(CustomerDet).filter(CustomerDet.username == username).count() == 1:
            update = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
            update.age = age
            update.gender = gender
            update.prevmedrcrds = prevmedrcrds
            update.address = address
            update.pincode = pincode
            db.session.commit()
            flash('Profile Created', 'success')
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('editprofile'))
    return render_template('add_profile.html')

@app.route('/editprofile', methods=['GET','POST'])
@is_logged_in
def editprofile():
    username = session['username']
    user = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    db.session.commit()
    if request.method == 'POST':
        age = request.form['age']
        if age != '':
            user.age = age
        prevmedrcrds = request.form['prevmedrcrds']
        if prevmedrcrds != '':
            user.prevmedrcrds = prevmedrcrds
        address = request.form['address']
        if address != '':
            user.address = address
        pincode = request.form['pincode']
        if pincode != '':
            user.pincode = pincode
        gmail_id = request.form['gmail_id']
        if gmail_id != '':
            user.gmail_id = gmail_id
        db.session.commit()
        flash('Profile Updated','success')
        return redirect(url_for('dashboard'))
    return render_template('editprofile.html',profile = db.session.query(CustomerDet).filter(CustomerDet.username == username).all())

class Orders(db.Model):
    __tablename__ = 'orders'
    number = db.Column(db.Integer, primary_key=True)
    hptl_username_in_vicinity = db.Column(db.String(200))
    username_cust = db.Column(db.String(200))
    type = db.Column(db.String(50))
    address = db.Column(db.Text())
    namecust = db.Column(db.String(200))
    aadhar = db.Column((db.String(20)))
    age = db.Column(db.String(5))
    gender = db.Column(db.String(1))
    prevmedrcrds = db.Column(db.Text())
    def __init__(self, hptl_username_in_vicinity, username_cust, type, address, namecust, aadhar, age, gender, prevmedrcrds):
        self.hptl_username_in_vicinity = hptl_username_in_vicinity
        self.username_cust = username_cust
        self.type = type
        self.address = address
        self.namecust = namecust
        self.aadhar = aadhar 
        self.age = age
        self.gender = gender
        self.prevmedrcrds = prevmedrcrds

@app.route('/accident')
@is_logged_in
def accident():
    username = session['username']
    list_of_hosp_to_send_message = []
    profile = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    hospital_to_send_request = db.session.query(RegisterMnmg).filter_by(pincode = profile.pincode).all() 
    db.session.commit()
    for hospital in hospital_to_send_request:
        list_of_hosp_to_send_message.append(hospital.username)
    if profile is not None:
        if list_of_hosp_to_send_message != []:
            if db.session.query(Orders).filter(Orders.username_cust == username).count() == 0:
                type='Accident'
                #send to all hospitals at the same time
                for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                    data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.namecust, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                    db.session.add(data)
                    db.session.commit()
                return render_template('request_sent.html')
            else:
                flash('you have already sent a request, kindly wait till it is processed','danger')
                return render_template('request_sent.html')
        else:
            return render_template('sorry.html')
    else:
        flash('Please fill in your details so that we can send it to the hospitals','danger')
        return redirect(url_for('add_profile'))
    return render_template('request_sent.html')

@app.route('/heartattack')
@is_logged_in
def heartattack():
    username = session['username']
    list_of_hosp_to_send_message = []
    profile = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    hospital_to_send_request = db.session.query(RegisterMnmg).filter_by(pincode = profile.pincode).all() 
    db.session.commit()
    for hospital in hospital_to_send_request:
        list_of_hosp_to_send_message.append(hospital.username)
    if profile is not None:
        if list_of_hosp_to_send_message != []   :
            if db.session.query(Orders).filter(Orders.username_cust == username).count() == 0:
                type='Heart Attack'
                #send to all hospitals at the same time
                for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                    data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.namecust, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                    db.session.add(data)
                    db.session.commit()
                return render_template('request_sent.html')
            else:
                flash('you have already sent a request, kindly wait till it is processed','danger')
                return render_template('request_sent.html')
        else:
            return render_template('sorry.html')
    else:
        flash('Please fill in your details so that we can send it to the hospitals','danger')
        return redirect(url_for('add_profile'))
    return render_template('request_sent.html')

@app.route('/otherailments')
@is_logged_in
def otherailments():
    username = session['username']
    list_of_hosp_to_send_message = []
    profile = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    hospital_to_send_request = db.session.query(RegisterMnmg).filter_by(pincode = profile.pincode).all() 
    db.session.commit()
    for hospital in hospital_to_send_request:
        list_of_hosp_to_send_message.append(hospital.username)
    if profile is not None:
        if list_of_hosp_to_send_message != []:
            if db.session.query(Orders).filter(Orders.username_cust == username).count() == 0:
                type='Other Ailments'
                #send to all hospitals at the same time
                for hptl_username_in_vicinity in list_of_hosp_to_send_message:
                    data = Orders(hptl_username_in_vicinity, username, type, profile.address, profile.namecust, profile.aadhar, profile.age, profile.gender, profile.prevmedrcrds)
                    db.session.add(data)
                    db.session.commit()
                return render_template('request_sent.html')
            else:
                flash('you have already sent a request, kindly wait till it is processed','danger')
                return render_template('request_sent.html')
        else:
            return render_template('sorry.html')
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
    aadhar = db.Column(db.String(20))
    age = db.Column(db.String(5))
    gender = db.Column(db.String(1))
    prevmedrcrds = db.Column(db.Text())

    def __init__(self, name_of_hptl_accepting_responsibilty, username_cust, type, address, namecust, aadhar, age, gender, prevmedrcrds):
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
   help = db.session.query(Orders).filter(Orders.hptl_username_in_vicinity == username).first()
   db.session.commit()
   if help is None:
       flash("you have no one to save","success")
       return render_template('dashboardmnmg.html')
   else:
       return render_template('dashboardmnmg.html', profile = db.session.query(Orders).filter(Orders.hptl_username_in_vicinity == username).all())
   return render_template('dashboardmnmg.html')

@app.route('/accepted/<username>')
@is_logged_in
def accepted(username):
    if db.session.query(Orders).filter(Orders.username_cust == username).count() > 0:
        acc_or_dec = "a"
        name_of_hptl_result = session['name']

        message = f"<p>{name_of_hptl_result} has accepted to help you. They will arrive to your place soon.</p>"
        user = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
        gmail_id = user.gmail_id

        #send mail to that person!!!!! important
        emailsend(gmail_id, message)
        
        #add data to past orders
        user_order = db.session.query(Orders).filter(Orders.username_cust == username).first()
        data = PastOrders(name_of_hptl_result, user_order.username_cust, user_order.type, user_order.address, user_order.namecust, user_order.aadhar, user_order.age, user_order.gender, user_order.prevmedrcrds)
        db.session.add(data)

        #delete data from orders
        edhavudhu = db.session.query(Orders).filter(Orders.username_cust == username).delete()
        db.session.commit()

        flash('You have accepted to save '+user.namecust, 'success')
        return redirect(url_for('dashboardmnmg'))
    return render_template('dashboardmnmg.html')

@app.route('/declined/<username>')
@is_logged_in
def declined(username):
    if db.session.query(Orders).filter(Orders.username_cust == username).count() > 0:
        acc_or_dec = "d"
        name_of_hptl_result = session['name']

        message = f"<p>{name_of_hptl_result} has declined to help you. We are sorry.</p>"
        user = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
        gmail_id = user.gmail_id

        #send mail to that person!!!!! important
        #emailsend(gmail_id, message)
        try:
            emailsend(gmail_id, message)
        except:
            flash('The person had registered with an invalid email. Could not deliver the message.', 'danger')

        #delete data from orders
        user_order = db.session.query(Orders).filter(Orders.username_cust == username, Orders.hptl_username_in_vicinity == name_of_hptl_result).first()
        db.session.delete(user_order)
        db.session.commit()
        
        flash('You have declined to save '+user.namecust, 'danger')
        return redirect(url_for('dashboardmnmg'))
    return render_template('dashboardmnmg.html')

@app.route('/patienthistory')
@is_logged_in
def patienthistory():
   username = session['name']
   help = db.session.query(PastOrders).filter(PastOrders.name_of_hptl_accepting_responsibilty == username).first()
   db.session.commit()
   if help is None:
       flash("you have not saved anyone yet","danger")
       return render_template('patienthistory.html', profile = db.session.query(PastOrders).filter(PastOrders.name_of_hptl_accepting_responsibilty == username).all())
   else:
       return render_template('patienthistory.html', profile = db.session.query(PastOrders).filter(PastOrders.name_of_hptl_accepting_responsibilty == username).all())
   return render_template('patienthistory.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('home'))

# Shivaram proj
class profileformhos(db.Model):
    __tablename__ = 'staffdetails'
    name = db.Column(db.String(200))
    age = db.Column(db.String(20))
    gender = db.Column(db.String(4))
    salary = db.Column(db.String(10))
    docid = db.Column(db.Integer, primary_key=True)
    spec = db.Column(db.String(200))
    hospitalid = db.Column(db.String(200))

    def __init__(self, name, age, gender, salary, spec, hospitalid):
        self.name = name
        self.age = age
        self.gender = gender
        self.salary = salary
        self.spec = spec
        self.hospitalid = hospitalid


@app.route('/addprofile_hos', methods=['GET','POST'])
@is_logged_in
def addprofile_hos():
    username = session['username']
    if request.method =='POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        salary = request.form['salary']
        spec = request.form['spec']
        hospitalid = username
        if db.session.query(profileformhos).filter(profileformhos.name == name).count() != 0:
            userdata = db.session.query(profileformhos).filter(profileformhos.name == name).first()
            if userdata.age == age and userdata.gender == gender and userdata.salary == salary and userdata.spec == spec and userdata.hospitalid == hospitalid:
                flash('Worker already exists','danger')
                return redirect(url_for('hosdetails'))
        else:
            data = profileformhos(name, age, gender, salary, spec, hospitalid)
            db.session.add(data)
            db.session.commit()
            flash('Profile Created', 'success')
            return redirect(url_for('hosdetails'))
    return render_template('addprofile_hos.html')

@app.route('/editprofilehos/<docid>', methods=['GET','POST'])
@is_logged_in
def editprofilehos(docid):
    user = db.session.query(profileformhos).filter(profileformhos.docid == docid).first()
    db.session.commit()
    if request.method == 'POST':
        name = request.form['name']
        if name != '':
            user.name = name
        age = request.form['age']
        if age != '':
            user.age = age
        gender = request.form['gender']
        if gender != '':
            user.gender = gender
        salary = request.form['salary']
        if salary != '':
            user.salary = salary
        spec = request.form['spec']
        if spec != '':
            user.spec = spec
        '''hospitalid = request.form['hospitalid']
        if hospitalid != '':
            user.hospitalid = hospitalid'''
        db.session.commit()
        flash('Profile Updated','success')
        return redirect(url_for('hosdetails'))
    return render_template('editprofilehos.html',profile = db.session.query(profileformhos).filter(profileformhos.docid == docid).all())

@app.route('/deletedoc/<docid>',methods=['GET','POST'])
def deletedoc(docid):
    data = db.session.query(profileformhos).filter(profileformhos.docid == docid).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('hosdetails'))

@app.route('/hosdetails', methods=['GET','POST'])
@is_logged_in
def hosdetails():
    username = session['username']
    help = db.session.query(profileformhos).filter(profileformhos.hospitalid == username).first()
    db.session.commit()
    return render_template('doctors.html', custdata = db.session.query(profileformhos).filter(profileformhos.hospitalid == username).all())

@app.route('/displaytables/<number>',methods=['GET','POST'])
def displaytables(number):
    session['number'] = number
    if number == '1':
        return render_template('displaytables.html', registermnmg = db.session.query(RegisterMnmg).all())
    elif number == '2':
        return render_template('displaytables.html', customerdet = db.session.query(CustomerDet).all())
    elif number == '3':
        return render_template('displaytables.html', orders = db.session.query(Orders).all())
    elif number == '4':
        return render_template('displaytables.html', pastorders = db.session.query(PastOrders).all())
    elif number == '5':
        return render_template('displaytables.html', ProfileFormHos = db.session.query(profileformhos).all())
    else:
        flash("No such table exists","danger")
        return redirect(url_for('home'))
    return render_template('displaytables.html')
    
if __name__=='__main__':
    app.run() 