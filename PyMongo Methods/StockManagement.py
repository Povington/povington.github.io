#code in python
import datetime
import json
from bson import json_util
from pymongo import MongoClient

#Create connection to db and collection
connection = MongoClient('localhost',27017)
db = connection['market']
collection = db['stocks']

#Tries to insert a document. If failed returns error
def insert_document(document):
      try:
        result=collection.save(document)
      except ValidationError as ve:
        abort(400, str(ve))
        return result
#Finds document using defined key value pair. Retuns error if now document found    
def get_document(key, value):
  document = collection.find_one({key:value})
  if not document:
    abort(404, 'No document with %s:%s' %key,value)
  return document

#Updates document found with key value pair. 
#Updats new values specified in document. Returns error if no document found.
def update_document(key, value, document):
  result = collection.update({key:value},{'$set':document}, upsert=False, multi=False)
  if not result:
    abort(404, 'No document with %s:%s' %key,value)
  return json.loads(json.dumps(result, indent=4, default=json_util.default))

#Deletes document found with key and value pair. 
#Deletes only first document. Returns error if no document found.
def delete_document(key, value):
  result = collection.delete_one({key:value})
  if not result:
    abort(404, 'No document with %s:%s' %key, value)
  return result

#Simple main function for testing.
def main():
  stockDocument = {       "Ticker" : "AZYX",
        "Earnings Date" : datetime.datetime.utcnow(),
        "Company" : "Povington's Python Testing",
        "50-Day Simple Moving Average" : -0.0055}
  print insert_document(stockDocument)
  
  print get_document("Ticker","AZYX")
  
  newValues = {"Volume" : 8675309}
  
  print update_document("Ticker","AZYX",newValues)
  
  print delete_document("Ticker","AZYX")
main()
