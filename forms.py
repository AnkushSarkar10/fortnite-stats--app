from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField , SubmitField , SelectField
from wtforms.validators import DataRequired , Length , Email , EqualTo , InputRequired , ValidationError
from models import Player
import requests



class AddPlayerForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
	platform = SelectField('Platform', choices=[('psn', 'Playstation'), ('xb1', 'Xbox'), ('pc', 'PC')])
	submit = SubmitField('Add Player')
	
	# to check if the user is already there
	def validate_username(self, username):
		user = Player.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is there. Please use a diffferent one.')
	#  to check if the user exists
	def check_if_user_exists(self,username,platform):
		headers = {'TRN-Api-Key':'1182a843-7f64-4ea2-a950-b9640218042c'}
		url = 'https://api.fortnitetracker.com/v1/profile/{}/{}'.format(platform.data,username.data)
		r = requests.get(url,headers=headers)
		data = r.json()
		if 'error' in data.keys():
			raise ValidationError('That user does not exist')
