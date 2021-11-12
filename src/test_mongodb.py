from pymongo import MongoClient
import certifi
from mongodbcredentials import CONNECTION_STRING

client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

for database_name in client.list_database_names():
    print(database_name)
    


