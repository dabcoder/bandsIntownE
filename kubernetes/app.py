from flask import Flask, render_template, request
from flask import url_for
from bandsintown import Client
from healthcheck import HealthCheck, EnvironmentDump

import urllib


app = Flask(__name__)


health = HealthCheck(app, "/healthcheck")

def website_available():
	code = urllib.urlopen("http://130.211.90.87:5000").getcode()
	print code
	if code == 200:
		return True, "Website up"
	else:
		return False, "Something is wrong!"

health.add_check(website_available)


@app.route('/')
def index_form():
    return render_template("index.html")

@app.route('/events', methods=['GET','POST'])
def event_form():
	if request.method == 'GET':
		return redirect(url_for('index_form'))
	name = request.form['artist'].lstrip()

	#Bandsintown API 
	client = Client('bitapp')
	events = client.events(name)
	
	event_list = {}
	if events != []:
		for event in events:
			event_list[event['formatted_location']] = event['formatted_datetime'] 
		return render_template('events.html', name=name, events=event_list)
	else:
		return render_template('nothing.html')


@app.errorhandler(500)
def page_not_found(e):
	return render_template('nothing.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0')