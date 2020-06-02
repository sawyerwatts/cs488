from query_setup import collection

over100 = collection.find({"recorded.speed" : {"$gt" : 100}}).count()

print("The number of records with a speed over 100 is", over100)

