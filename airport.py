# import 
import urllib.request
url = "https://raw.githubusercontent.com/"
"jpatokal/openflights/master/data/airports.dat"
response = urllib.request.urlopen(url)
data = response.read()

file = open("airports_db.dat", "wb")
file.write(data)
file.close()

import csv
f = open("airports_db.dat", encoding = "utf8")
airport_db = [] #main arrar for airport
errors = 0
for airport in csv.reader(f, delimiter = ','):
    current_record = []
    print(airport[0])
    try:
        #each slots containing information about an airport
        current_record.append(int(airport[0])) #airport ID
        current_record.append(airport[1]) 
        current_record.append(airport[2])
        current_record.append(airport[3])
        current_record.append(airport[4])
        current_record.append(airport[5])
        current_record.append(float(airport[6]))
        current_record.append(float(airport[7]))
        current_record.append(float(airport[8]))
        current_record.append(float(airport[9]))
        current_record.append(airport[10])
        current_record.append(airport[11])
        current_record.append(airport[12])
        current_record.append(airport[13])
    except : 
        errors += 1
    else:
        airport_db.append(current_record)
print("Total Airport Imported : ", len(airport_db),
 "# of Errors : ", errors)

url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
response= ""
data = ""
response = urllib.request.urlopen(url)
data = response.read()
file = open("routes_db.dat", "wb")
file.write(data)
file.close()

f = open("routes_db.dat", encoding = "utf8")
route_db = []
errors = 0
for route in csv.reader(f, delimiter = ','):
    current_record = []
    try:
        current_record.append(route[0]) 
        current_record.append(int(route[1]))
        current_record.append(int(route[3]))
        current_record.append(int(route[5]))
        current_record.append(int(route[7]))
        current_record.append(route[8])
  
    except : 
        errors += 1
    else:
        route_db.append(current_record)
print("Total Routes Imported : ", len(route_db), "# of Errors : ", errors)

import networkx as nx
network = nx.Graph()
print("network --> ", network)

for airport in airport_db:
    print("dooood")
    network.add_node(airport[0], id=airport[0], name=airport[1], city=airport[2], 
                        country=airport[3], iata=airport[4], 
                        icao=airport[5],
                        lat=airport[6], 
                        long=airport[7], 
                        alt=airport[8], offset=airport[9], 
                        daylight=airport[10], timezone=airport[11], 
                        type=airport[12], source=airport[13])

for route in route_db:
    if route[2] in network.nodes() and route[3] in network.nodes:
        network.add_edge(route[2], route[3], airline = route[0], 
                            airline_id = route[1], stops = route[4], 
                            equipment = route[5])
        

# print(network.nodes[507])
print("wtf")