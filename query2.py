from datetime import datetime
from query_setup import collection

total = 0
criteria = {
    "location.stationname": "Foster NB",
    "recorded.datetimerecorded": {
        "$gte": datetime(2011, 9, 21).timestamp() * 1000,
        "$lt" : datetime(2011, 9, 22).timestamp() * 1000
    }
}
for document in collection.find(criteria):
	volume = document["recorded"]["volume"]
	if volume is not None:
		total += volume

print("The total volume for Foster (NB) on 2011 Sept 21 is", total)
if total == 0:
    print("".join([
        "\tNOTE: total is zero; the test run does not have data of the ",
        "appropriate day, so that is why this may be empty."]))

