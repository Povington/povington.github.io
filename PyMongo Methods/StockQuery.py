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

##Takes input as key and value pair. 
#Counts outstanding shares and groups them by industry. Returns values in list. 
def aggregate_shares(key, value):
  pipeline = [
    {"$match" : {key:value}},
    {"$project" : {"Shares Outstanding": 1, "Industry" : 1}},
    {"$group" : {"_id" : "$Industry", "Shares Outstanding":{"$sum" : "$Shares Outstanding"}}}  
  ]
  result = collection.aggregate(pipeline)
  if not result:
    abort(404, 'No documents found..')
  print(list(result))

#Simple main function for testing
def main():
  h = 0.0055
  l = -0.0055
  print("Documents Found: ")
  print get_count("50-Day Simple Moving Average", h, l )
  
  print("Tickers pulled from query: ")
  print get_tickers("Industry", "Medical Laboratories & Research")
  
  print("Outstanding shares found in query: ")
  print aggregate_shares("Sector", "Basic Materials")
 
main()