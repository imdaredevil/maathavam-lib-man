#to create database and collection
from pymongo import MongoClient
import pymongo
import time
class database:
	client = MongoClient('localhost',27017)
	DB = client.libdb
	book = DB.book;
	user = DB.user
	lend = DB.lend
	@staticmethod
	def indexc():
		database.book.create_index([("bkid",pymongo.ASCENDING)],unique=True)
		database.user.create_index([("uid",pymongo.ASCENDING)],unique=True)
		database.lend.create_index([("bkid",pymongo.ASCENDING)],unique=True)
	@staticmethod
	def insert_book(bkid,bname):
		books = {}
		books['name'] = bname
		try:
			books['bkid'] = int(bkid)
		except ValueError:
			print("id should be a number");
			return;
		books['availability'] = 1;
		books['count'] = 0
		database.book.insert_one(books);
	@staticmethod
	def insert_user(uname,uid,phone):
		users = {}
		users["name"] = uname
		try:
			users["uid"] = int(uid)
		except ValueError:
			print("id should be a number")
			return;
		try:
			users["phone"] = int(phone)
		except ValueError:
			print("enter valid phone number")
			return;
		users['books'] = []
		print(users)
		database.user.insert_one(users);
	@staticmethod
	def lendbook(uid,bkid):
		da = time.time() + 15*24*60*60
		da = time.gmtime(da)
		if(type(bkid) == str):
			try:
				bkid = int(bkid)
			except ValueError:
				print("enter valid book id")
				return;
		if(type(uid) == str):
			try:
				uid = int(uid)
			except ValueError:
				print("enter valid user id")
				return;
		bo = list(database.book.find({"bkid":bkid}))
		if(bo == []):
			print("the book doesn't exist")
			return;
		bo = bo[0]
		bo["availability"] = 0
		database.book.update({"bkid":bkid},bo)
		u = list(database.user.find({"uid":uid}))
		if(u == []):
			print("the user is not registered")
			return;
		u = u[0]
		database.lend.insert_one({"bkid":bkid,"bookname":bo["name"],"uid":uid,"username":u["name"],"date":str(da)})
	@staticmethod
	def bookreturn(bkid):
		l = list(database.lend.find({"bkid":bkid}))
		if(l == []):
			print("this record is not in the db")
			return
		l = l[0]
		u = database.user.find_one({"uid":l["uid"]})
		bo = database.book.find_one({"bkid":bkid})
		bo["availability"] = 1
		bo["count"]+=1
		u["books"].append(bo["name"])
		database.lend.remove({"bkid":bkid})
		database.book.update({"bkid":bkid},bo)
		database.user.update({"uid":u["uid"]},u);
if __name__ == "__main__":
	database.indexc();
	#database.insert_book(100,"aryabhatta")
	#database.insert_user("cibi",120,9587600345)
	#database.lendbook(120,100);
	database.bookreturn(100)
	
			
	
	
