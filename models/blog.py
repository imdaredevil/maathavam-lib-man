import datetime
import uuid
from flask import session
from models.database import Database
def retblogs():
	blog_data = []
	coll=Database[blogs]
	for i in coll:
		blog_data.append(i)
	return blog_data
