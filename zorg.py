from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt as sa
import os
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

ENV = 'prod'
developer = 'Arjun'
if ENV == 'dev':
    app.debug = True
    app.config['SECRET_KEY'] = 'awwfaw'
    if developer == 'Arjun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgre-arj4703@localhost/Zorg'
    elif developer == 'Tarun':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Tarun@postgresql@localhost/Zorg'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hxceiafawftfoj:be308eb925667514c2f0102ea54672bd5b11a3c6643062b2012dedc396304b36@ec2-54-237-155-151.compute-1.amazonaws.com:5432/d82ngqr88afvm9'
    app.config['SECRET_KEY'] = os.environ['secret']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)

def emailsend(to,mssg):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '18cc8c2ea71e43'
    password = '27abc8c416d687'
    sender_email = 'zorg123546@gmail.com'
    message = MIMEText(mssg, 'html')
    message['Subject'] = 'Zorg'
    message['From'] = sender_email
    message['To'] = str(to)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login,password)
        server.sendmail(sender_email, to, message.as_string())

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORISED, Please Login','danger')
            return redirect(url_for('home'))
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORISED','danger')
            return redirect(url_for('home'))
    return wrap

@app.route('/', methods=['GET','POST'])
def home():
    if ENV == "dev":
        return redirect(url_for("index"))
    return render_template('preloader.html')

@app.route('/index', methods=['GET','POST'])
def index():
    session['ENV'] = ENV
    return render_template('index.html')

@app.route('/feedback', methods=['GET','POST'])
def feedback():
    if request.method == "POST":
        mailid = request.form['mailid']
        rating = request.form['rating']
        feedback = request.form['feedback']
        try:
            feed = rating + "\nFeedback Submitted:\n" + feedback
            emailsend(mailid, feed)
            flash('Your response has been recorded','success')
            if ENV == "dev":
                return redirect(url_for('index'))
            else:
                return redirect(url_for('home'))
        except:
            flash('Please enter all the details asked for','danger')
            return render_template('feedback.html')
        return render_template('feedback.html')
    return render_template('feedback.html')

@app.route('/route', methods=['GET','POST'])
def route():
    return render_template('route.html')

@app.route("/sitemap")
def sitemap():
    # Route to dynamically generate a sitemap of your website/application. lastmod and priority tags omitted on static pages. lastmod included on dynamic content such as blog posts.
    from flask import make_response, request, render_template
    import datetime
    from urllib.parse import urlparse
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc
    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {"loc": f"{host_base}{str(rule)}"}
                static_urls.append(url)
    # Dynamic routes with dynamic content
    try:
        dynamic_urls = list()
        blog_posts = Post.objects(published=True)
        for post in blog_posts:
            url = {"loc": f"{host_base}/blog/{post.category.name}/{post.url}", "lastmod": post.date_published.strftime("%Y-%m-%dT%H:%M:%SZ")}
            dynamic_urls.append(url)
        xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base)
    except:
        xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    return response

def username_predict(u,t):
    c = True
    while c:
        if not db.session.query(t).filter(t.username == u).count() == 0:
            x = random.randint(0,6000)
            u += str(x)
            s = ". Try " + u
            c = False
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

@app.route('/registercust', methods=['GET','POST'])
def registercust():
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
            data = CustomerDet(namecust, username, password, pincode, address, gmail_id, aadhar, age, gender, prevmedrcrds)
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
                return redirect(url_for('dashboardcust'))
            else:
                flash('Incorrect password','danger')
                return render_template('locust.html')
    else:
        return render_template('locust.html')

@app.route('/dashboardcust', methods=['GET','POST'])
@is_logged_in
def dashboardcust():
    username = session['username']
    custdata = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
    db.session.commit()
    if custdata.age == '' or custdata.gender == '' or custdata.prevmedrcrds == '' or custdata.address == '' or custdata.pincode == '':
        flash("Please fill these details","danger")
        return redirect(url_for('add_profile'))
    else:
        return render_template('dashboardcust.html', custdata = db.session.query(CustomerDet).filter(CustomerDet.username == username).all())
    return render_template('dashboardcust.html')

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
            return redirect(url_for('dashboardcust'))
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
        return redirect(url_for('dashboardcust'))
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
        try:
            emailsend(gmail_id, message)
        except:
            flash('The person had registered with an invalid email. Could not deliver the message.', 'danger')
        user_order = db.session.query(Orders).filter(Orders.username_cust == username).first()
        data = PastOrders(name_of_hptl_result, user_order.username_cust, user_order.type, user_order.address, user_order.namecust, user_order.aadhar, user_order.age, user_order.gender, user_order.prevmedrcrds)
        db.session.add(data)
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
        name_of_hptl_result = session['username']

        message = f"<p>{name_of_hptl_result} has declined to help you. We are sorry.</p>"
        user = db.session.query(CustomerDet).filter(CustomerDet.username == username).first()
        gmail_id = user.gmail_id
        try:
            emailsend(gmail_id, message)
        except:
            flash('The person had registered with an invalid email. Could not deliver the message.', 'danger')
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

class ProfileFormHos(db.Model):
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
        if db.session.query(ProfileFormHos).filter(ProfileFormHos.name == name).count() != 0:
            userdata = db.session.query(ProfileFormHos).filter(ProfileFormHos.name == name).first()
            if userdata.age == age and userdata.gender == gender and userdata.salary == salary and userdata.spec == spec and userdata.hospitalid == hospitalid:
                flash('Worker already exists','danger')
                return redirect(url_for('hosdetails'))
        else:
            data = ProfileFormHos(name, age, gender, salary, spec, hospitalid)
            db.session.add(data)
            db.session.commit()
            flash('Profile Created', 'success')
            return redirect(url_for('hosdetails'))
    return render_template('addprofile_hos.html')

@app.route('/editprofilehos/<docid>', methods=['GET','POST'])
@is_logged_in
def editprofilehos(docid):
    user = db.session.query(ProfileFormHos).filter(ProfileFormHos.docid == docid).first()
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
        db.session.commit()
        flash('Profile Updated','success')
        return redirect(url_for('hosdetails'))
    return render_template('editprofilehos.html',profile = db.session.query(ProfileFormHos).filter(ProfileFormHos.docid == docid).all())

@app.route('/deletedoc/<docid>',methods=['GET','POST'])
def deletedoc(docid):
    data = db.session.query(ProfileFormHos).filter(ProfileFormHos.docid == docid).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('hosdetails'))

@app.route('/hosdetails', methods=['GET','POST'])
@is_logged_in
def hosdetails():
    username = session['username']
    help = db.session.query(ProfileFormHos).filter(ProfileFormHos.hospitalid == username).first()
    db.session.commit()
    return render_template('doctors.html', custdata = db.session.query(ProfileFormHos).filter(ProfileFormHos.hospitalid == username).all())

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('home'))

#### ADMIN PROCESS ####

@app.route('/loginadmin', methods=['GET','POST'])
def loginadmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Administrator':
            if password == 'Administrator':
                session['admin'] = True
                return redirect(url_for('admindash'))
            else:
                flash('UNAUTHORISED','Danger')
                return redirect(url_for('home'))
        else:
            flash('UNAUTHORISED','Danger')
            return redirect(url_for('home'))
    return render_template('loginadmin.html')

@app.route('/admindash', methods=['GET','POST'])
@is_admin
def admindash():
    return render_template('admindash.html')

@app.route('/displaytables/<number>',methods=['GET','POST'])
@is_admin
def displaytables(number):
    session['number'] = number
    if number == "All":
        return render_template('displaytables.html', registermnmg = db.session.query(RegisterMnmg).all(), customerdet = db.session.query(CustomerDet).all(), orders = db.session.query(Orders).all(), pastorders = db.session.query(PastOrders).all(), profileformhos = db.session.query(ProfileFormHos).all())
    elif number == '1':
        return render_template('displaytables.html', registermnmg = db.session.query(RegisterMnmg).all())
    elif number == '2':
        return render_template('displaytables.html', customerdet = db.session.query(CustomerDet).all())
    elif number == '3':
        return render_template('displaytables.html', orders = db.session.query(Orders).all())
    elif number == '4':
        return render_template('displaytables.html', pastorders = db.session.query(PastOrders).all())
    elif number == '5':
        return render_template('displaytables.html', profileformhos = db.session.query(ProfileFormHos).all())
    else:
        flash("No such table exists","danger")
        return redirect(url_for('home'))
    return render_template('displaytables.html')

hospital_list = [['Newlife Hospital','newlife123','newlife123','123456','Chennai'],['Medwin Cares Hospital','medwin123','medwin123','321654','Vellore'],['Red Star Hospital','redstar123','redstar123','123456','Madurai'],['Angel Care Hospital','angel123','angel123','321654','Trichy']]
customer_list = [['1','James','james123','james123','123456','Chennai','james@mail.com','123456789123456','25','M','Fever'],['2','Mary','mary123','mary123','321654','Vellore','mary@mail.com','321654987321654','27','F','Cholera'],['3','John','john123','john123','123456','Madurai','john@mail.com','147258369147258','34','M','Diahorea'],['4','Julie','julie123','julie123','321654','Trichy','julie@mail.com','369258147369258','29','F','Jaundice']]
staff_list = [['David','34','M','50000','Cardiology','newlife123'],['Lisa','30','F','60000','Oncolgy','newlife123'],['Charles','47','M','55000','Neurology','newlife123'],['Karen','43','F','75000','Urology','newlife123'],['Thomas','44','M','65000','Gastroenterology','medwin123'],['Emily','41','F','60000','Gynaecology','medwin123'],['Donald','39','M','70000','Endocrinology','medwin123'],['Nancy','45','F','80000','Nephrology','medwin123'],['Gary','49','M','90000','Neurology','medwin123'],['Amy','38','F','85000','Physiotherapy','redstar123'],['Nick','31','M','80000','Psychiatry','redstar123'],['Carol','36','F','75000','Urology','redstar123'],['Ryan','40','M','70000','Ophthalmology','angel123'],['Helen','42','F','65000','Neonatology','angel123'],['Justin','44','M','80000','Anaesthesia','angel123'],['Emma','48','F','75000','ENT','angel123'],['Gary','51','M','65000','Dermatology','angel123']]

@app.route("/defaultable/<number>", methods=['GET','POST'])
@is_admin
def defaultable(number):
    session['number'] = number
    if number == "All":
        db.session.query(RegisterMnmg).delete()
        db.session.query(CustomerDet).delete()
        db.session.query(Orders).delete()
        db.session.query(PastOrders).delete()
        db.session.query(ProfileFormHos).delete()
        addreghospital(hospital_list)
        addregcustomer(customer_list)
        addhospitaldet(staff_list)
        db.session.commit()
    elif number == '1':
        db.session.query(RegisterMnmg).delete()
        addreghospital(hospital_list)
        db.session.commit()
    elif number == '2':
        db.session.query(CustomerDet).delete()
        addregcustomer(customer_list)
        db.session.commit()
    elif number == '3':
        db.session.query(Orders).delete()
        db.session.commit()
    elif number == '4':
        db.session.query(PastOrders).delete()
        db.session.commit()
    elif number == '5':
        db.session.query(ProfileFormHos).delete()
        addhospitaldet(staff_list)
        db.session.commit()
    else:
        flash("No such table exists","danger")
        return redirect(url_for('admindash'))
    return redirect(url_for('admindash'))

def addreghospital(hospital_list):
    if len(hospital_list) == 0:
        chumma = 0
    else:
        row = hospital_list[0]
        data = RegisterMnmg(row[0],row[1],sa.hash(row[2]),row[3],row[4])
        db.session.add(data)
        db.session.commit()
        list1 = []
        for i in range(len(hospital_list)):
            if i > 0:
                list1.append(hospital_list[i])
        addreghospital(list1)

def addregcustomer(customer_list):
    if len(customer_list) == 0:
        chumma = 0
    else:
        row = customer_list[0]
        data = CustomerDet(row[1],row[2],sa.hash(row[3]),row[4],row[5],row[6],row[7],row[8],row[9],row[10])
        db.session.add(data)
        db.session.commit()
        list2 = []
        for j in range(len(customer_list)):
            if j > 0:
                list2.append(customer_list[j])
        addregcustomer(list2)

def addhospitaldet(staff_list):
    if len(staff_list) == 0:
        chumma = 0
    else:
        row = staff_list[0]
        data = ProfileFormHos(row[0],row[1],row[2],row[3],row[4],row[5])
        db.session.add(data)
        db.session.commit()
        list3 = []
        for k in range(len(staff_list)):
            if k > 0:
                list3.append(staff_list[k])
        addhospitaldet(list3)

@app.route("/deletetables/<number>", methods=['GET','POST'])
@is_admin
def deletetables(number):
    if number == "All":
        db.session.query(RegisterMnmg).delete()
        db.session.query(CustomerDet).delete()
        db.session.query(Orders).delete()
        db.session.query(PastOrders).delete()
        db.session.query(StaffDet).delete()
        db.session.commit()
    elif number == '1':
        db.session.query(RegisterMnmg).delete()
        db.session.commit()
    elif number == '2':
        db.session.query(CustomerDet).delete()
        db.session.commit()
    elif number == '3':
        db.session.query(Orders).delete()
        db.session.commit()
    elif number == '4':
        db.session.query(PastOrders).delete()
        db.session.commit()
    elif number == '5':
        db.session.query(StaffDet).delete()
        db.session.commit()
    else:
        flash("No such table exists","danger")
        return redirect(url_for('admindash'))
    return redirect(url_for('admindash'))

@app.route("/deletetablerow/<number>", methods=['GET','POST'])
@is_admin
def deletetablerow(number):
    session['number'] = number
    if number == "All":
        return render_template('deletetablerow.html', registermnmg = db.session.query(RegisterMnmg).all(), customerdet = db.session.query(CustomerDet).all(), orders = db.session.query(Orders).all(), pastorders = db.session.query(PastOrders).all(), profileformhos = db.session.query(ProfileFormHos).all())
    elif number == '1':
        return render_template('deletetablerow.html', registermnmg = db.session.query(RegisterMnmg).all())
    elif number == '2':
        return render_template('deletetablerow.html', customerdet = db.session.query(CustomerDet).all())
    elif number == '3':
        return render_template('deletetablerow.html', orders = db.session.query(Orders).all())
    elif number == '4':
        return render_template('deletetablerow.html', pastorders = db.session.query(PastOrders).all())
    elif number == '5':
        return render_template('deletetablerow.html', profileformhos = db.session.query(ProfileFormHos).all())
    else:
        flash("No such table exists","danger")
        return redirect(url_for('admindash'))
    return render_template("deletetablerow.html")

@app.route("/deleterow/<chumma>", methods=['GET','POST'])
def deleterow(chumma):
    number = session['number']
    session['chumma'] = chumma
    if number == '1':
        data = db.session.query(RegisterMnmg).filter(RegisterMnmg.username == chumma).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('deletetablerow', number='1'))
    elif number == '2':
        data = db.session.query(CustomerDet).filter(CustomerDet.username == chumma).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('deletetablerow', number='2'))
    elif number == '3':
        data = db.session.query(Orders).filter(Orders.number == chumma).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('deletetablerow', number='3'))
    elif number == '4':
        data = db.session.query(PastOrders).filter(PastOrders.number == chumma).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('deletetablerow', number='4'))
    elif number == '5':
        data = db.session.query(ProfileFormHos).filter(ProfileFormHos.docid == chumma).first()
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('deletetablerow', number='5'))
    else:
        flash("No such table exists","danger")
        return redirect(url_for('admindash'))
    return render_template("deletetablerow.html")

@app.route('/logoutadmin')
@is_admin
def logoutadmin():
    session.clear()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run()
