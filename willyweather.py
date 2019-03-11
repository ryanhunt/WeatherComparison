#!/usr/local/bin/python3

import json
import time
import urllib

__author__ = "Ryan Hunt <ryan@ryanhunt.net>"
__copyright__ = "Copyright (c) 2016-2017 Ryan Hunt"

class willyweather():
	def __init__(self, key):
		self.apiKey = key
		
	def status(self):
		return "okay."
		
	def getApiKey(self):
		return self.apiKey
		
	def getLocationIDFromCoords(self, lat, long, units = "km"):
		#
		# https://www.willyweather.com.au/api/docs/v2.html#location-search-by-coordinates
		# https://api.willyweather.com.au/v2/{api key}/search.json?lat=-33.89&lng=151.27&units=distance:km
		#
		# {'units': {'distance': 'km'}, 'location': {'id': 4857, 'name': 'Oatley', 'region': 'Sydney', 'state': 'NSW', 'postcode': '2223', 'timeZone': 'Australia/Sydney', 'lat': -33.98143, 'lng': 151.08277, 'typeId': 1, 'distance': 0.6}}
		#
		#
		url = 'https://api.willyweather.com.au/v2/%s/search.json?lat=%s&lng=%s&units=distance:%s' % (self.apiKey, lat, long, units)
		#print(url)
		
		with urllib.request.urlopen(url) as url:
			data = json.loads(url.read().decode())
			
		return data['location']['id']
		
	def getCurrentConditions(self, key):
		#
		# https://www.willyweather.com.au/api/docs/v2.html#observational
		# https://api.willyweather.com.au/v2/{api key}/locations/4988/weather.json?observational=true
		#
		# Returns:
		# {'location': {'id': 4857, 'name': 'Oatley', 'region': 'Sydney', 'state': 'NSW', 'postcode': '2223', 'timeZone': 'Australia/Sydney', 'lat': -33.98143, 'lng': 151.08277, 'typeId': 1}, 'observational': {'observations': {'temperature': {'temperature': 34.3, 'apparentTemperature': 29.4, 'trend': 1}, 'delta-t': {'temperature': 15.4, 'trend': 1}, 'cloud': {'oktas': 0, 'trend': 0}, 'humidity': {'percentage': 17, 'trend': -1}, 'dewPoint': {'temperature': 5.8, 'trend': -1}, 'pressure': {'pressure': 996.7, 'trend': -1}, 'wind': {'speed': 20.4, 'gustSpeed': 25.9, 'trend': 0, 'direction': 315, 'directionText': 'NW'}, 'rainfall': {'lastHourAmount': 0, 'todayAmount': 0, 'since9AMAmount': 0}}, 'stations': {'temperature': {'id': 352, 'name': 'Canterbury', 'lat': -33.91, 'lng': 151.12, 'distance': 8.9}, 'humidity': {'id': 352, 'name': 'Canterbury', 'lat': -33.91, 'lng': 151.12, 'distance': 8.9}, 'dewPoint': {'id': 352, 'name': 'Canterbury', 'lat': -33.91, 'lng': 151.12, 'distance': 8.9}, 'pressure': {'id': 345, 'name': 'Sydney Airport', 'lat': -33.94, 'lng': 151.17, 'distance': 9.2}, 'wind': {'id': 352, 'name': 'Canterbury', 'lat': -33.91, 'lng': 151.12, 'distance': 8.9}, 'rainfall': {'id': 352, 'name': 'Canterbury', 'lat': -33.91, 'lng': 151.12, 'distance': 8.9}}, 'issueDateTime': '2019-02-12 13:10:00', 'units': {'temperature': 'c', 'amount': 'mm', 'speed': 'km/h', 'distance': 'km', 'pressure': 'hPa'}}}
		
		#
		url = 'https://api.willyweather.com.au/v2/%s/locations/%s/weather.json?observational=true' % (self.apiKey, key)
		#print(url)
		with urllib.request.urlopen(url) as url:
			data = json.loads(url.read().decode())
		d = data['observational']['observations']['temperature']
		#d = WeatherConditions(data)
		#return d
		return d
			