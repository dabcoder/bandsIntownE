import requests
import json

def event_list():
	name = raw_input('Artist? ')
	name = name.replace(" ", "%20")
	url = 'http://api.bandsintown.com/artists/' + name + '/events.json?api_version=2.0&app_id=SCSPY'
	headers = {'Content-type': 'application/json'}
	resp    = requests.post(url=url)
	concert_data = json.loads(resp.text)
	dict_concerts = {}
	for e in concert_data:
		dict_concerts[e['formatted_datetime']] = e['venue']['place'] + " - " + e['formatted_location']

	for date, location in dict_concerts.items():
		print date, " - " , location

print event_list()

