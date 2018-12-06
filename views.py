from flask import render_template , url_for , flash , redirect , request , abort
from models import Player
from myapp import app,db
from forms import AddPlayerForm
import requests

# functions and stuf required for the fortnite api to work

def check_for_stats(r):
	data = r.json()
	if 'error' in data.keys():
		return None
	else:
		return r.json()

def get_main_stats(data):
	if data != None:
		dict_of_stats = {}
		for i in data['lifeTimeStats']:
			if i['key'] == 'Wins':
				dict_of_stats['Wins'] = i['value']
			if i['key'] == 'Kills':
				dict_of_stats['Kills'] = i['value']
			if i['key'] == 'Matches Played':
				dict_of_stats['Matches Played'] = i['value']
		return dict_of_stats
	else:
		return None

def get_all_stats(data):
	if data != None:
		stats = {}
		
		stats["Solo Wins"] = data['stats']['p2']['top1']['value']
		stats["Solo Matches"] = data['stats']['p2']['matches']['value']
		stats["Solo Kills"] = data['stats']['p2']['kills']['value']
		stats["Solo K/D"] = data['stats']['p2']['kd']['displayValue']

		stats["Duo Wins"] = data['stats']['p10']['top1']['value']
		stats["Duo Matches"] = data['stats']['p10']['matches']['value']
		stats["Duo Kills"] = data['stats']['p10']['kills']['value']
		stats["Duo K/D"] = data['stats']['p10']['kd']['displayValue']

		stats["Squad Wins"] = data['stats']['p9']['top1']['value']
		stats["Squad Matches"] = data['stats']['p9']['matches']['value']
		stats["Squad Kills"] = data['stats']['p9']['kills']['value']
		stats["Squad K/D"] = data['stats']['p9']['kd']['displayValue']

		return stats
	else:
		return None

headers = {'TRN-Api-Key':'1182a843-7f64-4ea2-a950-b9640218042c'}
# proxies = {
#   'http': 'http://10.10.1.10:3128',
#   'https': 'http://10.10.1.10:1080',
# }
# routs
@app.route('/')
@app.route('/home/')
def home():
	players = Player.query.all()
	stats_list = []
	for player in players:
		url = 'https://api.fortnitetracker.com/v1/profile/{}/{}'.format(player.platform,player.username)
		r = requests.get(url,headers=headers)
		data = check_for_stats(r)
		# i know it might not be the best way to do it but this shit works
		if data != None:
			stats = get_main_stats(data)
			stats['Player']=str(player.username)
			stats['Platform']=str(player.platform)
			stats_list.append(stats)
		else:
			pass

	return render_template('home.html',players=players,stats_list=stats_list)
 
@app.route('/add_player',methods=['GET','POST'])
def add_player():
	form = AddPlayerForm()
	if form.validate_on_submit():
		url = 'https://api.fortnitetracker.com/v1/profile/{}/{}'.format(form.platform.data,form.username.data)
		r = requests.get(url,headers=headers)
		data = r.json()
		if 'error' in data.keys():
			flash('That user does not exist','danger')
			return redirect(url_for('add_player'))
		else:
			player = Player(username=form.username.data,platform=form.platform.data)
			db.session.add(player)
			db.session.commit()
			flash('Player added!','success')
			return redirect(url_for('home'))
	return render_template('add_player.html',form=form)


@app.route('/player_stats/<platform>/<name>')
def player_stats(platform,name):
	url = 'https://api.fortnitetracker.com/v1/profile/{}/{}'.format(platform,name)
	r = requests.get(url,headers=headers)
	data = check_for_stats(r)
	stats_list = []
	stats = get_all_stats(data)
	stats_list.append(stats)

	return render_template('player_stats.html',stats_list=stats_list,
							name=name,platform=platform)