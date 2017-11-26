import codecs, os, pymongo
from models import msg

from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from functools import wraps
from pymongo import MongoClient
#<<<<<<< HEAD
import time
from time import strftime,gmtime,strptime

import bcrypt
app = Flask("maathavam-lib-man")

MONGO_URL='mongodb://mani:mani@ds121014.mlab.com:21014/liibrary'
print(MONGO_URL)
client=pymongo.MongoClient(MONGO_URL)
db=client.library
# Index
@app.route('/')
def index():

	book = db.book
	user = db.user
	lend = db.lend
	book.create_index([("bkid",pymongo.ASCENDING)],unique=True)
	user.create_index([("uid",pymongo.ASCENDING)],unique=True)
	lend.create_index([("bkid",pymongo.ASCENDING)],unique=True)
	return render_template('home.html',value='')


@app.route('/login')
def login():
    return render_template('login.html')
#>>>>>>> 539166723692c174104c91dda63bda1c37cce855

@app.route('/auth/login',methods=['POST','GET'])
def login_template():
	#print 'entered login'
	users=db.users
	#print users
	login_user=users.find_one({'uname':request.form['uname']})
	if login_user :
		if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password'].encode('utf-8')) ==login_user['password'].encode('utf-8') :
			session['uname']=request.form['uname']
			session['logged_in']=True
			flash('You are now logged in', 'success')
			return redirect(url_for('dashboard'))
	return render_template('home.html',value='Invalid User Name or Password')		
	
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['POST','GET'])
def regis():
	return render_template('register.html')

@app.route('/auth/register', methods=['POST','GET'] )
def register_template():
	#return str(request.form['passkey']=="shankar")
	if request.method =='POST' and request.form['passkey']=="shankar":
		#print mongo
		users=db['users']
		#print users
		existing_user=users.find_one({'uname':request.form['uname']})
		#print existing_user
		if existing_user == None:
			hashpass=bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
#<<<<<<< HEAD
			#print hashpass,users
			db['users'].insert({'uid':request.form['uid'],'name':request.form['name'],'uname':request.form['uname'],'password':hashpass,'phone':request.form['phone']})
			session['uname']=request.form['uname']
			#print 'inserted'
#=======
			print (hashpass,users)
			db['users'].insert({'uid':request.form['uid'],'name':request.form['name'],'uname':request.form['uname'],'password':hashpass,'phone':request.form['phone']})
			session['uname']=request.form['uname']
			#print 'inserted'
#>>>>>>> 539166723692c174104c91dda63bda1c37cce855
			return 'registerd as '+request.form['name']
			return render_template('login.html')
		return render_template('home.html',value="user already registered")
	return render_template('home.html',value="Invalid Passkey Contact maadhavam")

@app.route('/post')
@is_logged_in
def post():
	return render_template('fillpost.html')


@app.route('/add/posts',methods=['POST','GET'])
@is_logged_in
def add_post():
	if request.method=="POST":
		post=db['posts']
		post.insert({'title':request.form['title'],'desc':request.form['desc'],'author':request.form['author']})
		return redirect(url_for('article'))


# About
@app.route('/about')
@is_logged_in
def about():
	content=db['content']
	v=content.find({})
	s=[]
	for i in v:
		s.append(i)
#<<<<<<< HEAD
	#print  s
#=======
	#print  s
#>>>>>>> 539166723692c174104c91dda63bda1c37cce855
	return render_template('about.html',values=s)


@app.route('/article')
def article():
	pst=db['posts']
	l=[]
	v=pst.find({})
	for i in v:
		l.append(i)
	return render_template('article.html',articles=l)
#<<<<<<< HEAD
@app.route('/give',methods=['POST','GET','PULL'])
def lend():
	#print request.method
	if request.method == "GET":
		return render_template('lendp.html')
	if request.method == "POST":
		bkid = request.form['bkid']
		uid = request.form['uid']
		book = db.book
		user = db.user
		lend = db.lend
		da = time.time() + 15*24*60*60
		da = time.localtime(da)
		try:
			bkid = int(bkid)
		except ValueError:
			return "enter valid book id"
		try:
			uid = int(uid)
		except ValueError:
			return ("enter valid user id")
		bo = list(book.find({"bkid":bkid,"availability":1}))
		if(bo == []):
			return ("the book doesn't exist")
		bo = bo[0]
		bo["availability"] = 0
		book.update({"bkid":bkid},bo)
		u = list(user.find({"uid":uid}))
		if(u == []):
			return "the user is not registered";
		u = u[0]
		lend.insert_one({"bkid":bkid,"bookname":bo["name"],"uid":uid,"username":u["name"],"date":strftime("%d %b %y",da)})
		return render_template('home.html',value = str(bo["name"]) + " should be return back by " + strftime("%d %b %y",da))
@app.route('/adduser',methods=['POST','GET'])
def insert_user():
	if request.method == 'GET':
		return render_template("adduser.html")
	uid = request.form["uid"]
	uname = request.form["uname"]
	phone = request.form["phone"]
	user = db.user
	users = {}
	users["name"] = uname
	try:
		users["uid"] = int(uid)
	except ValueError:
		return "id should be a number"
	try:
		users["phone"] = int(phone)
	except ValueError:
		return ("enter valid phone number")
	users['books'] = []
	users["logmem"] = seesion["uname"]
	print(users)
	user.insert_one(users);
	return render_template("home.html",value="successfully added")
@app.route('/addbook',methods=['POST','GET'])
def insert_book():
	if request.method == 'GET':
		return render_template("addbook.html")
	bkid = request.form["bkid"]
	bname = request.form["bname"]
	book = db.book
	books = {}
	books['name'] = bname
	try:
		books['bkid'] = int(bkid)
	except ValueError:
		return "id should be a number";
	books['availability'] = 1;
	books['count'] = 0
	book.insert_one(books);
	return render_template("home.html",value="successfully added")
@app.route('/return',methods=['POST','GET'])
def return1():
	if request.method == 'GET':
		return render_template("return.html")
	bkid = request.form["bkid"]
	bkid = int(bkid);
	book = db.book
	user = db.user
	lend = db.lend
	l = list(lend.find({"bkid":bkid}))
	if(l == []):
		return ("this record is not in the db")
	l = l[0]
	u = user.find_one({"uid":l["uid"]})
	bo = book.find_one({"bkid":bkid})
	bo["availability"] = 1
	bo["count"]+=1
	u["books"].append(bo["name"])
	lend.remove({"bkid":bkid})
	book.update({"bkid":bkid},bo)
	user.update({"uid":u["uid"]},u);
	return render_template("home.html",value = bo["name"] + " returned")

@app.route('/msglist')
def msgli():
	lend = db.lend
	user = db.user
	today = time.time()
	q=msg.sms(8072257509,'secret005')
	defaulters = []
	lis = lend.find()
	for li in lis:
		tempdate=strptime(li["date"],"%d %b %y")
		tempdate = time.mktime(tempdate)
		if(today>tempdate):
			defaulters.append(li)
			u = user.find_one({"uname":li['username']}) 
			#print("hello")
			n=q.send(u['phone'],"Please return the book taken from maadhavam")
			if(n == False):
				return render_template("home.html",value="msg failed")
	q.logout()
	return render_template("msg.html",users=defaulters)
	
#=======


#>>>>>>> 539166723692c174104c91dda63bda1c37cce855
if __name__ == '__main__':
	app.secret_key = 'secretkey'	
	app.run(debug=True)

