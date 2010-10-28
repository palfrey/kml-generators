#!/usr/bin/python

from xml.dom.minidom import  parseString
import urlgrab

cache = urlgrab.Cache(cache=".cache")
data = cache.get("http://borisapi.heroku.com/stations.xml").read()

tree = parseString(data)

print (
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
   '<Document>\n'
   )
 
for station in tree.getElementsByTagName("station"):
	
	placemark = (
	'<Placemark>\n'
	   '<name>%s</name>\n'
	   '<Point>\n'
	   '<coordinates>%f,%f</coordinates>\n'
	   '</Point>\n'
	   '</Placemark>\n'
	) % (station.getElementsByTagName("name")[0].firstChild.data.replace("&","&amp;"),
		float(station.getElementsByTagName("long")[0].firstChild.data),
		float(station.getElementsByTagName("lat")[0].firstChild.data)
		)
	print placemark
	#break

print '</Document></kml>'
