#!/usr/local/bin/python3

from accuweather import *
from willyweather import *
from openweathermap import *
from geopy.geocoders import Nominatim
from geopy.geocoders import Bing
import datetime
import csv
from tqdm import tqdm

#a = AccuWeather(ACCUWEATHER_API_KEY)
w = willyweather(WILLWEATHER_API_KEY)
a = AccuWeather(ACCUWEATHER_API_KEY) 
o = OpenWeatherMap(OPENWEATHERMAP_API_KEY)


#geolocator = Nominatim(user_agent=NOMINATIM_USER_AGENT)
geolocator = Bing(BING_API_KEY)
#addresses = []


results = []

# postcode, version, suburb, state
# 0800,800,DARWIN,NT

#with open("addresses.csv", "r") as f:
with open("au-suburbs-postcodes.csv", "r") as f:
    num_rows = sum(1 for line in f)
    
#with open("addresses.csv", "r") as infile:
with open("au-suburbs-postcodes.csv", "r") as infile:
	reader = csv.reader(infile)
	next(reader)
	for row in tqdm(reader, total = num_rows-1):
		# process each row
		#country = row[0]
		country = "AU"
		address = row[2] + " " + row[3] + " " + row[0]
		#address = row[1]
		
		try:
			location = geolocator.geocode(address)
		except:
			location = None
			pass
		#print((location.latitude, location.longitude))
		
		#print ("Got this for %s: %s" % (address, location))

		
		if (location):
		
			wKey = w.getLocationIDFromCoords(location.latitude, location.longitude)
			
			#print("wKey for %s is: %s" % (address, wKey))
			
			aKey = a.getLocationIDFromCoords(location.latitude, location.longitude)
			
			#print("aKey for %s is: %s" % (address, aKey))
			#data = a.getCurrentConditions(aKey)
			wData = w.getCurrentConditions(wKey)
			oData = o.getCurrentConditions(location.latitude, location.longitude)
			
			if (aKey):
				conditions = a.getCurrentConditions(aKey)
			else:
				conditions = None
				
			
		
		timestamp = datetime.datetime.now()
		
		if (location and conditions):
			data = {'timestamp': timestamp, 'country': country, 'address': address, 'lat': location.latitude, 'long': location.longitude, 'accuweather': conditions.getTemperature(), 'willyweather': wData['temperature'], 'openweathermap': oData}
		else:
			data = {'timestamp': timestamp, 'country': country, 'address': address, 'lat': 0, 'long': 0, 'accuweather': 0, 'willyweather': 0, 'openweathermap': 0}
			
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