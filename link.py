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

	rs = xml.getElementsByTagName("RecordSet")[0]
	records = rs.getElementsByTagName("Record")
	for record in records:
		atm = {}
		fields = record.getElementsByTagName("Field")
		for field in fields:
			if not field.firstChild:
				content = ""
			else:
				content = field.firstChild.data
			name = field.getAttribute("name")
			atm[name] = content

			atm["lat"] = float(record.getElementsByTagName("Lat")[0].firstChild.data)
			atm["lon"] = float(record.getElementsByTagName("Lon")[0].firstChild.data)
		yield atm

def kml_gen_atms(lat=51.51856,lon=-0.14377,maxDistance=3,max_results=50):
	atms = {}
	for atm in gen_link_atms(lat=lat,lon=lon,maxDistance=maxDistance,max_results=max_results):
		if atm.has_key("surcharge_value") and int(atm["surcharge_value"])>0:
			continue
		#print atm
		atms[atm["institution_name"]+", "+atm["street"]] = (atm["lon"], atm["lat"])
	return atms

if __name__ == "__main__":
	print kml_string(kml_gen_atms())

