import sys
import urllib2
import json

def getGeocodingKey():
	geoFile = open("../Keys/geocoding.txt","r")
	key = geoFile.read()
	return key
	

def getLatLong(query):
	base = "https://maps.googleapis.com/maps/api/geocode/json?address="
	base += query
	base += "&key="+key
	res = urllib2.urlopen(base).read()
	json_data = json.loads(res)
	lat_long = json_data["results"][0]["geometry"]["location"]
	return lat_long["lat"],lat_long["lng"]

try:
 address = sys.argv[1]
except IndexError:
	print "Insufficient number of arguments passed: "+str(len(sys.argv))
	print "Requires an argument"
	sys.exit()

address = address.strip()
address = address.replace(" ","+")

key = getGeocodingKey()

# Testing
lat, lng = getLatLong(address)

print "Latitude: "+str(lat)
print "Longitude: "+str(lng)

