from datetime import datetime
from query_setup import collection


# Query 3:
# Single-Day Station Travel Times: Find travel time for station Foster NB for 5-minute 
# intervals for Sept 22, 2011. Report travel time in seconds.


# Get total travel time for Foster NB
def foster_nb_travel_time(start, end):
    total_length = 0
    length = 0
    total_speed = 0
    speed = 0
    num_speeds = 0
    avg_speed = 0 
    # Query for Foster NB and given start/end times 
    criteria = {
      "location.stationname": "Foster NB",
      "recorded.datetimerecorded": {
        "$gte": start.timestamp() * 1000,
        "$lte": end.timestamp() * 1000
      }
    }
    
    # Loop through each document/entry in the collection with the given criteria
    for document in collection.find(criteria): 
        # Add length if it isn't null 
        length = document["location"]["stationlength"]
        if length is not None:
            total_length += length
        # Add speed if it isn't null
        speed = document["recorded"]["speed"]
        if speed is not None:
            total_speed += speed 	 
            num_speeds += 1

    # Calculate average speed         
    avg_speed = total_speed/num_speeds
    # Returns total travel time in seconds 	
    return (total_length/avg_speed)*3600 
       

# Get total travel time in seconds for each 5 minute interval for 24 hours from station Foster NB
def query3():
    hour = 0
    # Set start and end to be  9/22/2011 at 12 am
    start = datetime(2011, 9, 22, 0, 0)
    end = datetime(2011, 9, 22, 0, 0)
    # Time constants
    min_per_hour = 60
    hours_per_day = 24
   
    # For each hour in the day 
    for hour in range(0, hours_per_day):
        # For each 5 minute interval
        for minute in range(0, min_per_hour, 5):
            start = end
            # Move to next hour 
            if(minute >= 60):
                hour += 1
                minute = 0
            end = datetime(2011, 9, 22, hour, minute) 
            print(start)
            print("Travel time for this interval (in seconds): " + str(foster_nb_travel_time(start, end)))
    


    return 

# Run query 
query3()

