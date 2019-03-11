#!/usr/local/bin/python3

import json
import time
import urllib
from urllib.error import URLError, HTTPError
import sys

__author__ = "Ryan Hunt <ryan@ryanhunt.net>"
__copyright__ = "Copyright (c) 2016-2017 Ryan Hunt"

class AccuWeather():
	def __init__(self, key):
		self.apiKey = key
		
	def status(self):
		return "okay."
		
	def getApiKey(self):
		return self.apiKey
			
		
	def getLocationIDFromCoords(self, lat, long):
		#
		# https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/geoposition/search
		#
		url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=%s&q=%s%s%s' % (self.apiKey, lat, "%2C%20",long)
		#print(url)
		
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
		except HTTPError as e:
			if (e.code == 503):
				print("It appears you've hit your daily limit of 50 requests for Accuweather. Try again tomorrow pal.")
				#sys.exit(0)
			return None
			
		return data['Key']
		
	def getCurrentConditions(self, key):
		#
		# https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D
		#
		# Returns:
		# [{'LocalObservationDateTime': '2019-02-11T15:39:00+11:00', 'EpochTime': 1549859940, 'WeatherText': 'Sunny', 'WeatherIcon': 1, 'HasPrecipitation': False, 'PrecipitationType': None, 'IsDayTime': True, 'Temperature': {'Metric': {'Value': 28.9, 'Unit': 'C', 'UnitType': 17}, 'Imperial': {'Value': 84.0, 'Unit': 'F', 'UnitType': 18}}, 'MobileLink': 'http://m.accuweather.com/en/au/oatley/17365/current-weather/17365?lang=en-us', 'Link': 'http://www.accuweather.com/en/au/oatley/17365/current-weather/17365?lang=en-us'}]
		#
		url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s' % (key, self.apiKey)
		#print(url)
		try:
			with urllib.request.urlopen(url) as url:
				data = json.loads(url.read().decode())
			d = WeatherConditions(data)
		except:
			d = None
			pass
		return d
		
class WeatherConditions():
	def __init__(self, json):
		self.json = json
		self.setUnits("c")
		
	def setUnits(self, units="c"):
		if (units.lower() == "c" ) or (units.lower() == "f"):
			self.units = units.lower()
		else:
			return 0
			
	def getTemperature(self):
		if (self.units == "c"):
			return self.json[0]['Temperature']['Metric']['Value']
		else:
			return self.json[0]['Temperature']['Imperial']['Value']
			
	def isRaining(self):
		if (self.json[0]['HasPrecipitation'] == "False"):
			return 0
		else:
			return 1
		