#!/usr/bin/python
import json
import bottle
from bottle import route, run, request, abort
from pymongo import MongoClient

connection = MongoClient('localhost',27017)
db = connection['city']
collection = db['inspections']


# set up URI paths for REST service
@route('/stocks/api/v1.0/createStock', method='POST') # Sets endpoint with POST method
#Simple add document function that reads request line. Aborts if not data requested.
def addDocument():
  data = request.body.readline()
  if not data():
    abort(400, 'No data received!')
  document = json.loads(data)
  if not document.has_key('Ticker'):
    abort(400, 'No Ticker specified')
  try:
    insert_document(document)
  except ValidationError as ve:
    abort(400, str(ve))
   

@route('stocks/api/v1.0/getStock', method='GET')  #Sets endpoint with GET method
#Simple get document function that searches databas by Ticker
def getDocument():
  request.query.Ticker #sets query to look for Ticker
  Ticker=request.query.Ticker
  if Ticker:
    #make calls to database from here
    query="{\"Ticker\" : "+request.query.Ticker+"}"
  else:
    abort(400, 'No data received')

  document = collection.find_one(query)#finds a document based on query criteria
  return document

  for x in document:
    print(x)

@route('/stocks/api/v1.0/updateStock', method='GET')  #Sets endpoint with GET method
#Simple update function that finds document based on Ticker Key. Updates based on result requested. 
def updateDocument():
  oldDocument = get_document("Ticker",request.query.Ticker)
  
  document = update_document(request.query.Ticker, request.query.result, oldDocument)
  
  if not document:
    abort(404, 'Update error %s' %request.query.result)
  return json.loads(json.dumps(document, indent=4, default=json_util.default))
    
@route('/stocks/api/v.10/deleteStock', method='GET')  #Sets endpoint with GET method
#Simple Delete function that finds and deletes a document based on Ticker.
def deleteDocument():
  document = delete_document("Ticker", request.query.Ticker)
  
  if not document:
    abort (404, 'Delete Error: %s' %request.query.Ticker)
  return json.loads(json.dumps(document, indent=4, default=json_util.default))

@route('/stocks/api/v1.0/getTickers', method='GET')
def getTickers():
  for document in collection.find("{\"Industry\" : "+request.query.industry+"}"):
    if not document:
      abort(404, 'No document with Key Value pair' )
    return document

@route('/stocks/api/v1.0/getShares', method='GET')
#aggregate function that searches database by sector value. projects outstanding shares and groups by industry. 
def aggregateShares():
  pipeline = [
    {"$match" : {"Sector": request.query.sector}},
    {"$project" : {"Shares Outstanding": 1, "Industry" : 1}},
    {"$group" : {"_id" : "$Industry", "Shares Outstanding":{"$sum" : "$Shares Outstanding"}}}  
  ]
  result = collection.aggregate(pipeline)
  if not result:
    abort(404, 'No documents found..')
  print(list(result))

@route('/stocks/api/v1.0/stockReport', method='POST')
#Function to create a stock report. Stock tickers to the end of read_result. 
def getReport():
  read_result = []
  for tickerSymbol in request.json.list:
    read_result.append(read_document({"Ticker" : tickerSymbol}))
  print (read_result)
  if(isinstance(read_result, Exception)):
    print('exception')
    abort(500, "Database Error")
  return json.dumps(read_result, sort_keys=True, indent=4, default=json.default)

@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
#Function that searches database based on industry and returns top five stocks in the industry. 
def portfolio(industry = None):
  try:
    pipeLine = [{"$match":{"Industry":industry}},
                {"$project":{"Company":1,"Price":1}},
                {"$sort":{"Price":-1}},{"$limit":5}]
    stockResults = list(db.stocks.aggregate(pipeLine))
    return json.dumps(stockResults, indent=4, default=json_util.default)
  
  except NameError:
    abort (404, 'No parameter for id %s' %id)
    
if __name__ == '__main__': #declare instance of request
  #app.run(debug=True)
  run(host='0.0.0.0' , port=8080)
