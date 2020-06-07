from datetime import datetime
from query_setup import collection


#Single-Day Station Travel Times: Find travel time for station Foster NB for 5-minute intervals for Sept 22, 2011. Report travel time in seconds.

print(collection)

# Get total travel time for Foster NB
def foster_nb_travel_time(start, end):
    total_length = 0
    length = 0
    total_speed = 0
    speed = 0
    criteria = {
      "location.stationname": "Foster NB",
      "recorded.datetimerecorded": {
        "$gte": start.timestamp() * 1000,
        "$lte": end.timestamp() * 1000
      }
    }

    for document in collection.find(criteria):
       # if length is None:
        length = document["location"]["stationlength"]
        total_length += length

        speed = document["recorded"]["speed"]
        #if speed is not None:
        total_speed += speed 	
	
	# Returns total travel time 	
        return total_length/total_speed


def interval_time(num_minutes):
    return 


# Start at 9/22/2011 at 12 am
start = datetime(2011, 9, 22, 0, 0)
# End at 9/22/2011 at 11:59 pm
end = datetime(2011, 9, 22, 23, 59)

print(foster_nb_travel_time(start, end))



#for document in collection.find(criteria):
#	print(document)
	
#collection.find()
#print(station)
#get_total_travel_time();

