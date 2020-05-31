from pymongo import MongoClient
from pprint import pprint

client = MongoClient(port=27017)
db = client.freewaydata

over100 = db.oneHour.find({"recorded.speed" : {"$gte" : 100}}).count()

pprint(over100)
