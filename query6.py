from query_setup import collection

#finds a route from the starting station to Columbia Blvd
def findRoute(station):
	#base case
	if station == "Columbia to I-205 NB":
		return station 
	#look through documents for the next station on our route
	else:
		print(station)
		for document in collection.find({"location.stationname": station}):
			station = document["location"]["nextstationname"]
			break
		input()
		return findRoute(station)

startStation = "Johnson Cr NB"
endStation = findRoute(startStation)
print(endStation)
