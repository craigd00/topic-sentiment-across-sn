import pymongo
from pymongo import MongoClient
import certifi

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://craig:Dissertation2021-22@socialmediadatasets.rjayn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
from pymongo import MongoClient
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

# Create the database for our example (we will use the same database throughout the tutorial
for db_info in client.list_database_names():
    print(db_info)
    


