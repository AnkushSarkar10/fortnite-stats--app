from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)


# cofigs baby!
app.config.from_pyfile('config.py') 

# database object
db = SQLAlchemy(app)


# app needs to be created before we import views.py
from views import *

if __name__=="__main__":
	app.jinja_env.cache = {}
	app.run(debug=True)
