"""
main module which starts the application
"""

import os
import utils
from json import load
from argparse import ArgumentParser
from flask import Flask, render_template, jsonify, make_response, request
from dbUtils import meta, addQuery, showDbData


# initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey4CoWinHawk!'


# Custom Config
cowin_config = dict()


def parseCommandLineArgs():
	"""  initialize parser for global config
	"""
	parser = ArgumentParser() 
	# adding arguments and defaults
	parser.add_argument("-d", "--debug", help = "Debug mode", default=False)
	parser.add_argument("-i", "--hostIp", help = "Host address", default='0.0.0.0')
	# Read arguments from command line and return
	args = parser.parse_args()
	return args


def lastUpdateTime(folder):
	"""  returns the latest last updated timestamp of all the static files 
	"""
	return str(max(os.path.getmtime(os.path.join(root_path, file)) \
		for root_path, dirs, files in os.walk(folder) \
			for file in files))


@app.route('/')
def index():
	"""  Serve the initial landing page. This comes from flask
	"""
	return render_template('dashboard.html', 
			total_users=100, 
			helped_users=73,
			last_updated=lastUpdateTime('static/'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""  This will register a new user in the app
	"""
	if request.method == 'GET':
		return render_template('register.html', 
			last_updated=lastUpdateTime('static/'))
	else:
		try:
			requestData = request.get_json()
			addQuery(requestData)
		except Exception as ex:
			return make_response(str(ex), 400)
		else:
			make_response("Request Accepted", 200)



@app.route('/details')
def details():
	""" This will return the details of all registered users
	"""
	return render_template('status.html', 
			last_updated=lastUpdateTime('static/'))


@app.route('/api/getpininfo/<int:pincode>', methods = ['GET'])
def getPinInfo(pincode = None):
	"""  Gets Info about the given pincode {"district" : "district_name", "state" : "state_name"}
	"""
	data, status = utils.custom_request(cowin_config['pinInfo_host'], cowin_config['url_getPinInfo'],  urlParams = {'pincode':pincode})
	if data is not None and len(data) > 0:
		if data[0]['Status'] == 'Success':
					return jsonify({
						'district' : data[0]['PostOffice'][0]['District'], 
						'state' : data[0]['PostOffice'][0]['State']
					})
		else:
			return jsonify({'district' : 'NA', 'state' : 'NA'})
	else:
		return make_response(status, 400)


@app.route('/api/states', methods = ['GET'])
def getStates():
	"""  Returns the list of states as list of {"state_id" : "state_name"}
	"""
	data, status = utils.custom_request(cowin_config['cowin_host'], cowin_config['url_getAllStates'])
	if data is not None and 'states' in data:
		return jsonify(data['states'])
	else:
		return make_response(status, 400)


@app.route('/api/districts/<int:state_id>', methods = ['GET'])
def getDistricts(state_id = None):
	"""  Returns the list of Districts for the State Id as list of {"district_id" : "district_name"}
	"""
	data, status = utils.custom_request(cowin_config['cowin_host'], cowin_config['url_getDistByState'], urlParams = {'state_id':state_id} )
	if data is not None and 'districts' in data:
		return jsonify(data['districts'])
	else:
		return make_response(status, 400)
		

if __name__ == '__main__':
	args = parseCommandLineArgs()
	cowin_config.update(utils.read_jsonFile('./config.json'))
	meta.create_all()
	app.run(host=args.hostIp, debug=args.debug)
