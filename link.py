#!/usr/bin/python

from xml.dom.minidom import parseString
import urlgrab
from kml import kml_string
import json
from StringIO import StringIO
import re
from sys import exit

cache = urlgrab.Cache(cache=".cache")
cache.user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.9) Gecko/20100501 Iceweasel/3.5.9 (like Firefox/3.5.9)"

api = cache.get("http://clients.multimap.com/API/maps/1.2/linkapi/")
cookies = api.headers.cookies()

deliveryID = int(cookies["deliveryId"])
mdin = int(cookies["MDIN"])

initial = cache.get("http://clients.multimap.com/API/geocode/1.2/linkapi?output=json&callback=MMGeocoder.prototype._GeneralJSONCallback&locale=en-us&qs=w1a%%201aa&countryCode=GB&deliveryID=%d&identifier=0"%deliveryID, ref="http://www.link.co.uk/Style%20Library/ATMLocator.html", headers={"cookie":"mdin=%d"%mdin}).read()
data = cache.get("http://clients.multimap.com/API/search/1.2/linkapi?output=json&callback=MMSearchRequester.prototype._GeneralJSONCallback&dataSource=mm.clients.linkapi&count=50&lat=51.51856&lon=-0.14377&maxDistance=3000&orderByFields=distance&orderByOrder=asc&locale=en-us&deliveryID=%d&identifier=1"%deliveryID, ref="http://www.link.co.uk/Style%20Library/ATMLocator.html", headers={"Cookie":"MDIN=%d"%mdin}).read()

sf = StringIO(data[data.find("{"):data.find(")")])
j = json.load(sf)

try:
	print j['record_sets']['mm.clients.linkapi']['total_record_count']
except:
	print j
