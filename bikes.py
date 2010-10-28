#!/usr/bin/python

from xml.dom.minidom import parseString
import urlgrab
from kml import kml_string

cache = urlgrab.Cache(cache=".cache")
data = cache.get("http://borisapi.heroku.com/stations.xml").read()

tree = parseString(data)
places = {}
for station in tree.getElementsByTagName("station"):
	places[station.getElementsByTagName("name")[0].firstChild.data.replace("&","&amp;")] = \
		(float(station.getElementsByTagName("long")[0].firstChild.data),
		float(station.getElementsByTagName("lat")[0].firstChild.data))

print kml_string(places)
