## Feel Free to take a look at what I've been working on below:


Here's a quick  [Code Review](https://youtu.be/B3gvz-9SsJYI) performed on an authentication page I've been working on. Check it out!

You can take a look at the full authentication page project [here.](https://github.com/Povington/povington.github.io/tree/master/Authentication%20Page)

### Other Projects

Take a look below to see a few other scripts and apps that I have created.

For example, here's an example of some PyMongo methods I have been working on. . 

#code in python
import datetime
import json
from bson import json_util
from pymongo import MongoClient

#Create connection to db and collection
connection = MongoClient('localhost',27017)
db = connection['market']
collection = db['stocks']

#Takes input for key, high and low values. 
#Returns count of documents that fall between high and low values      
def get_count(key, high, low):
  result = collection.count({key: {'$lte' : high, '$gte' : low}})
  if not result:
    abort(404, 'No document with %s' %key)
  return result

#Takes input as key and value pair. 
#Queries db and returns "Ticker" value for documents that match query criteria
def get_tickers(key, value):
  for document in collection.find({key:value}, {"_id" : 0, "Ticker" : 1}):
    if not document:
      abort(404, 'No document with %s:%s' %key,value)
    return document

You can see all the methods I've been creating [here](https://github.com/Povington/povington.github.io/tree/master/PyMongo%20Methods)

I've also been creating some powershell scripts to help with system management. Take a look [here](https://github.com/Povington/povington.github.io/blob/master/TempFolderManagement.ps1) to see an example.

### Thank you for taking the time to check out my page and work. 


