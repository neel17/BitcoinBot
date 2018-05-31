import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


# A decorator that tells Flask what URL should trigger our function
# By default, the flask route responds to the GET requests.
# This prefrence can be altered by providing methods argument to route() decorator.

@app.route('/webhook', methods=['POST'])
def webhook():
	# Parse the incoming JSON request data and returns it.
	# By default this function will return None if the mumetype is not application/json but this can be overridden by the force parameter.
	# force - if set to True the mimetype is ignored
	# silent - if set to True this methid will fall silently and return None
	
	req = request.get_json(silent=True, force=True)

	print(json.dumps(req, indent=4))
	
	# Extract paprameter value --> query the Open Weather API --> construct response --> send to Dialogflow
	res = makeResponse(req)
	res = json.dumps(res, indent = 4)
	# Setup the response from webhook in right format
	r = make_response(res) 
	r.headers['Content-type'] = 'application/json'
	return r
	
# Helper function makeResponse

def makeResponse(req):
	# For V1 API Call
	#result = req.get('result')
	
	# For V2 API Call
	result = req.get('queryResult') 
	parameters = result.get('parameters')
	bitcoin = parameters.get('bitcoin')
	date = parameters.get('date-time')
	
	# Condition for extrating the date-time attributes
	if 'startDate' in date:
	#if date.get('startDate'):
		start_date = date.get('startDate')[:10]
		end_date = date.get('endDate')[:10]
	else:
		start_date = date[:10]
		end_date = date[:10]
		query_flag = 'single'
	
	base_url = 'https://api.coindesk.com/v1/bpi/historical/close.json?'
	load_url = 'start=' + start_date + '&end=' + end_date
	url = base_url + load_url
	r = requests.get(url)
	json_object = r.json()
	output_json = json_object['bpi']
	
	out = []
	for i,j in output_json.items():
		out.append(str(i) + " : "+str('$') +str(j)) 
	
	
	
	
			
	# The response from the service should have the following fields:
	# Name : speech ; displayText ; source
	# Type : string ; string ; string
	# Description : Response to the request
	# Text displayed on the user device screen ;  Data Source
	
	speech = "The Bitcoin price  " + '\n'.join(out)
	
	return{
	# V1 return format
	#"speech":speech,
	#"displayText":speech,
	#"source":"apiai-weather-webhook"
	
	# V2 return format
	"fulfillmentText":speech,
	"fulfillmentText":speech,
	"source":"apiai-weather-webhook"
	
	}
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))
	print("Starting app on port %d" % port)
	app.run(debug=False, port=port, host='0.0.0.0')
	
	
