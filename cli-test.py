#!/usr/local/bin/python3

from accuweather import *
from willyweather import *
from openweathermap import *
from geopy.geocoders import Nominatim
from geopy.geocoders import Bing
import datetime
import csv
from tqdm import tqdm
import os

#a = AccuWeather(os.environ.get('ACCUWEATHER_API_KEY'))
w = willyweather(os.environ.get('WILLYWEATHER_API_KEY'))
a = AccuWeather(os.environ.get('ACCUWEATHER_API_KEY'))
o = OpenWeatherMap(os.environ.get('OPENWEATHERMAP_API_KEY'))


#geolocator = Nominatim(user_agent=os.environ.get('NOMINATIM_USER_AGENT'))
geolocator = Bing(os.environ.get('BING_API_KEY'))
#addresses = []


results = []

# postcode, suburb, state, lat, lon
# 0800,DARWIN,NT, x, y

#with open("addresses.csv", "r") as f:
with open("au-suburbs-postcodes-coords.csv", "r") as f:
    num_rows = sum(1 for line in f)
    
#with open("addresses.csv", "r") as infile:
with open("au-suburbs-postcodes-coords.csv", "r") as infile:
	reader = csv.reader(infile)
	next(reader)
	for row in tqdm(reader, total = num_rows-1):
		# process each row
		#country = row[0]
		country = "AU"
		address = row[1] + " " + row[2] + " " + row[0]
		#address = row[1]
		
		#
		#try:
		#	location = geolocator.geocode(address)
		#except:
		#	location = None
		#	pass
		##print((location.latitude, location.longitude))
		#
		##print ("Got this for %s: %s" % (address, location))

		lat = row[3]
		lon = row[4]
		
		wKey = w.getLocationIDFromCoords(lat, lon)
			
		#print("wKey for %s is: %s" % (address, wKey))
		
		aKey = a.getLocationIDFromCoords(lat, lon)
		
		#print("aKey for %s is: %s" % (address, aKey))
		#data = a.getCurrentConditions(aKey)
		wData = w.getCurrentConditions(wKey)
		oData = o.getCurrentConditions(lat, lon)
		
		if (aKey):
			conditions = a.getCurrentConditions(aKey)
		else:
			conditions = None
				
			
		
		timestamp = datetime.datetime.now()
		
		if (conditions):
			data = {'timestamp': timestamp, 'country': country, 'address': address, 'lat': lat, 'long': lon, 'accuweather': conditions.getTemperature(), 'willyweather': wData['temperature'], 'openweathermap': oData}
		else:
			data = {'timestamp': timestamp, 'country': country, 'address': address, 'lat': lat, 'long': lon, 'accuweather': 0, 'willyweather': wData['temperature'], 'openweathermap': oData}
			
		results.append(data)
		
		with open("results.csv.tmp", 'a') as output_file:
		    dict_writer = csv.DictWriter(output_file, data)
		    dict_writer.writerow(data)
		    output_file.close()
		
		#time.sleep(1)
		
		#print ("At %s the temp at %s is: %sC (Accuweather), %sC (WillyWeather), %sC (OpenWeatherMap)" % (data['timestamp'], data['address'], data['accuweather'], data['willyweather'], data['openweathermap'] ))	
		
keys = results[0].keys()
with open("results.csv", 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)	
    
print ('Results saved to results.csv')
			


#for i, val in enumerate(addresses):