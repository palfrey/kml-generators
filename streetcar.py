#!/usr/bin/python

from xml.dom.minidom import parseString
import urlgrab
from kml import kml_string

cache = urlgrab.Cache(cache=".cache")
data = cache.get("http://www.streetcar.co.uk/LocationsXml.xml").read()

tree = parseString(data)
places = {}
for table in tree.getElementsByTagName("Table"):
	places[table.getElementsByTagName("LN")[0].firstChild.data] = \
		(float(table.getElementsByTagName("WLo")[0].firstChild.data),
		float(table.getElementsByTagName("WLa")[0].firstChild.data))

print kml_string(places)
