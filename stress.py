import math
from kml import kml_string
from sys import stderr,argv
 
# code from http://www.johndcook.com/python_longitude_latitude.html
def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
	
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
	
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
	
    # Compute spherical distance from spherical coordinates.
	
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi&#39; cos(theta-theta&#39;) + cos phi cos phi&#39;
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6373 # gets us into km

start_point = 0,0
point_dist = 0.02 # km

delta = point_dist/distance_on_unit_sphere(0,0,1,0)

square = int(argv[1])
max_items = square*square
print >>stderr, square, max_items

places = {}
for x in range(int(-math.floor(square/2)), int(math.ceil(square/2))):
	for y in range(int(-math.floor(square/2)), int(math.ceil(square/2))):
		curr = (start_point[0] + (delta*x),start_point[1]+(delta*y))
		places["%d,%d"%(x,y)] = curr

print kml_string(places)
