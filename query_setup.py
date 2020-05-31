from pymongo import MongoClient
import sys

client = MongoClient(port=27017)
db = client.freewaydata
collection = None

if len(sys.argv) == 1:
    pass
else:
    collection = db.oneHour

