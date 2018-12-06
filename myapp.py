from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy 
from boto.s3.connection import S3Connection
import os

app = Flask(__name__)

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

# cofigs baby!
app.config.from_pyfile('config.py') 

# database object
db = SQLAlchemy(app)


# app needs to be created before we import views.py
from views import *

if __name__=="__main__":
	app.jinja_env.cache = {}
	app.run(debug=True)
