# Query 5: Peak Period Travel Times: Find the average travel time for 7-9 AM 
# and 4-6 PM on September 22, 2011 for the I-205 NB freeway. Report travel time in minutes.

# Sawyer/Medina/Ramon's functionality for query4 with an additional argument
from datetime import datetime
from query_setup import collection


def station_travel_time(station, start, end):
    avg_time = 0
    total_speed = 0
    length = None
    count = 0
    criteria = {
        "location.stationname": station,
        "recorded.datetimerecorded": {
            "$gte": start.timestamp() * 1000,
            "$lt" : end.timestamp() * 1000
        }
    }

    for document in collection.find(criteria):
        if length is None:
            length = document["location"]["stationlength"]

        speed = document["recorded"]["speed"]
        if speed is not None:
            total_speed += speed
            count += 1

    avg_speed = total_speed/count
    avg_time = (length/avg_speed)*60
    return avg_time



# Dylan's function for query 6
#finds a route from the starting station to Columbia Blvd
def findRoute(station, start, end):
    global total_avg   

    #base case
    if station == "Columbia to I-205 NB":
        print(station)
        avg_time = station_travel_time(station, start, end)
        print("".join([
             "The average travel time (min) " + str(station) + " from ", str(start),
             " to ", str(end), " is ", str(avg_time) 
        ]))
        total_avg += avg_time
        return  

    #look through documents for the next station on our route
    else:
        print(station)
        for document in collection.find({"location.stationname": station}):
            # get average travel time for this station
            avg_time = station_travel_time(station, start, end)
            print("".join([
                "The average travel time (min) " + str(station) + " from ", str(start),
                " to ", str(end), " is ", str(avg_time)
            ]))
            print()
            total_avg += avg_time
            station = document["location"]["nextstationname"]
            break
        return findRoute(station, start, end)
      

def query5(station, start, end):
    avg_time = None
    try:
       # avg_time = station_travel_time(stationname, start, end)
        findRoute(station, start, end)
    except ZeroDivisionError:
        print("".join([
            "There are no recorded occurences of data from ", str(start), " to ",
            str(end)
        ]))
        print("".join([
            "\tNOTE: the test run does not have data of the ",
            "appropriate day, so that is why this may be empty."
        ]))
        print()
    finally:
      # here is where we should deal with the Columbia station I think
        print("".join([
            "The average travel time for I-205 NB from ", str(start),
            " to ", str(end), " is ", str(total_avg), " minutes."
        ]))
   

total_avg = 0
start = datetime(2011, 9, 22, 7, 0)
end   = datetime(2011, 9, 22, 9, 0)
query5("Sunnyside NB", start, end)

print()

total_avg = 0
start = datetime(2011, 9, 22, 16, 0)
end   = datetime(2011, 9, 22, 18, 0)
query5("Sunnyside NB", start, end)
