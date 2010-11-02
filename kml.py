def kml_string(places):
	ret = '<?xml version="1.0" encoding="UTF-8"?>\n' \
   + '<kml xmlns="http://www.opengis.net/kml/2.2">\n' \
   + '<Document>\n'
 
	for place in places.keys():
		(lon, lat) = places[place]
		placemark = (
		'<Placemark>\n'
		   '<name>%s</name>\n'
		   '<Point>\n'
		   '<coordinates>%f,%f</coordinates>\n'
		   '</Point>\n'
		   '</Placemark>\n'
		) % (place.replace("&", "&amp;"),lon,lat)
		ret += placemark

	return ret +'</Document></kml>'
