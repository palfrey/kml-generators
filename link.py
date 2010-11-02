#!/usr/bin/python

from xml.dom.minidom import parseString
import urlgrab
from kml import kml_string
import xml
import re
from sys import exit,stderr

def gen_link_atms(lat=51.51856,lon=-0.14377,maxDistance=3,max_results=50):
	cache = urlgrab.Cache(cache=".cache")
	cache.user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.9) Gecko/20100501 Iceweasel/3.5.9 (like Firefox/3.5.9)"

	api = cache.get("http://clients.multimap.com/API/maps/1.2/linkapi/")
	cookies = api.headers.cookies()

	deliveryID = int(cookies["deliveryId"])
	mdin = int(cookies["MDIN"])

	data = cache.get("http://clients.multimap.com/API/search/1.2/linkapi?output=xml&callback=MMSearchRequester.prototype._GeneralJSONCallback&dataSource=mm.clients.linkapi&count=%d&lat=%f&lon=%f&maxDistance=%d&orderByFields=distance&orderByOrder=asc&locale=en-us&deliveryID=%d&identifier=1"%(max_results,lat,lon,maxDistance,deliveryID), ref="http://www.link.co.uk/Style%20Library/ATMLocator.html", headers={"Cookie":"MDIN=%d"%mdin}, timeout=240).read()

	xml = parseString(data)

	atms = {}
	rs = xml.getElementsByTagName("RecordSet")[0]
	records = rs.getElementsByTagName("Record")
	for record in records:
		fields = record.getElementsByTagName("Field")
		institution = ""
		street = ""
		skip = False
		for field in fields:
			if field.firstChild:
				content = field.firstChild.data
			else:
				continue
			name = field.getAttribute("name")
			if name == "surcharge_value":
				if int(content)>0:
					skip = True
					break
			elif name == "street":
				street = content
			elif name == "institution_name":
				institution = content
		if skip:
			continue

		lat = float(record.getElementsByTagName("Lat")[0].firstChild.data)
		lon = float(record.getElementsByTagName("Lon")[0].firstChild.data)

		atms[institution+", "+street] = (lon, lat)
	return atms

print kml_string(gen_link_atms())

