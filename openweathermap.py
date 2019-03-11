#!/usr/local/bin/python3

import json
import time
import urllib

__author__ = "Ryan Hunt <ryan@ryanhunt.net>"
__copyright__ = "Copyright (c) 2016-2017 Ryan Hunt"

class OpenWeatherMap():
	def __init__(self, key):
		self.apiKey = key
		
	def status(self):
		return "okay."
		
	def getApiKey(self):
		return self.apiKey
		
	def getCurrentConditions(self, lat, long, units="metric"):
		#
		# api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}
		#
		# Returns: {'coord': {'lon': 151.08, 'lat': -33.99}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 35.44, 'pressure': 996, 'humidity': 11, 'temp_min': 35, 'temp_max': 36}, 'visibility': 10000, 'wind': {'speed': 10.8, 'deg': 310, 'gust': 15.9}, 'clouds': {'all': 0}, 'dt': 1549938600, 'sys': {'type': 1, 'id': 9600, 'message': 0.0042, 'country': 'AU', 'sunrise': 1549913241, 'sunset': 1549961515}, 'id': 2206004, 'name': 'Connells Point', 'cod': 200}
		# 
		
		#
		url = 'https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s&units=%s' % (lat, long, self.apiKey, units)
		#print(url)
		with urllib.request.urlopen(url) as url:
			data = json.loads(url.read().decode())
		d = data['main']['temp']
		return d