from myapp import db , app
from flask_login import UserMixin

class Player(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable= False)
	platform = db.Column(db.String(3), nullable= False)
	
	def __repr__(self):
 		return ("Username : {} Platform : {}".format(self.username,self.platform))
