from datetime import datetime
from query_setup import collection


def foster_nb_travel_time(start, end):
    avg_time = 0
    total_speed = 0
    length = None
    count = 0
    criteria = {
        "location.stationname": "Foster NB",
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
    avg_time = (length/avg_speed)*3600
    return avg_time


def query4(start, end):
    avg_time = None
    try:
        avg_time = foster_nb_travel_time(start, end)
        print("".join([
            "The average travel time (sec) for Foster NB from ", str(start),
            " to ", str(end), " is ", str(avg_time)
        ]))
    except ZeroDivisionError:
        print("".join([
            "There is no recorded occurences of data from ", str(start), " to ",
            str(end)
        ]))
        print("".join([
            "\tNOTE: the test run does not have data of the ",
            "appropriate day, so that is why this may be empty."
        ]))


start = datetime(2011, 9, 22, 7, 0)
end   = datetime(2011, 9, 22, 9, 0)
query4(start, end)

print()

start = datetime(2011, 9, 22, 16, 0)
end   = datetime(2011, 9, 22, 18, 0)
query4(start, end)

