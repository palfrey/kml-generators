#!/usr/bin/python

from xml.dom.minidom import parseString
import urlgrab
from kml import kml_string
import json
#import jsonlib
#import cjson
from StringIO import StringIO
import re
from sys import exit,stderr

cache = urlgrab.Cache(cache=".cache")
cache.user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.9) Gecko/20100501 Iceweasel/3.5.9 (like Firefox/3.5.9)"

api = cache.get("http://clients.multimap.com/API/maps/1.2/linkapi/")
cookies = api.headers.cookies()

deliveryID = int(cookies["deliveryId"])
mdin = int(cookies["MDIN"])

data = cache.get("http://clients.multimap.com/API/search/1.2/linkapi?output=json&callback=MMSearchRequester.prototype._GeneralJSONCallback&dataSource=mm.clients.linkapi&count=50&lat=51.51856&lon=-0.14377&maxDistance=3000&orderByFields=distance&orderByOrder=asc&locale=en-us&deliveryID=%d&identifier=1"%deliveryID, ref="http://www.link.co.uk/Style%20Library/ATMLocator.html", headers={"Cookie":"MDIN=%d"%mdin}, timeout=240).read()

sf = StringIO(data[data.find("{"):data.rfind(")")])
try:
	j = json.load(sf)
	#j = jsonlib.read(data[data.find("{"):data.rfind(")")])
	#j = cjson.decode(data[data.find("{"):data.rfind(")")])
except Exception,e:
	open("dump","wb").write(data)
	raise

try:
	atms = {}
	print >>stderr, j['record_sets']['mm.clients.linkapi']['total_record_count']
	print >>stderr, len(j['record_sets']['mm.clients.linkapi']['records'])
	for record in j['record_sets']['mm.clients.linkapi']['records']:
		if int(record[u'surcharge_value'])>0:
			continue
		atms[record[u'institution_name']+", "+record[u'street']] = (float(record[u'point'][u'lon']),float(record[u'point'][u'lat']))
	print kml_string(atms)
except Exception, e:
	print >>stderr,e
	print j
