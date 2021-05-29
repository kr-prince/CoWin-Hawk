import os
import argparse
from flask import Flask, render_template

# initialize Flask and SocketIO
app = Flask(__name__)


def parseCommandLineArgs():
	# initialize parser for global config
	parser = argparse.ArgumentParser() 
	# adding arguments and defaults
	parser.add_argument("-d", "--debug", help = "Debug mode", default=False)
	parser.add_argument("-i", "--hostIp", help = "Host address", default='0.0.0.0')
	# Read arguments from command line and return
	args = parser.parse_args()
	return args

def lastUpdateTime(folder):
	# This function returns the latest last updated timestamp of all the static files 
	return str(max(os.path.getmtime(os.path.join(root_path, file)) \
		for root_path, dirs, files in os.walk(folder) \
			for file in files))


@app.route('/')
def index():
	# Serve the initial landing page. This comes from flask
	return render_template('dashboard.html', 
			total_users=100, 
			helped_users=73,
			last_updated=lastUpdateTime('static/'))

@app.route('/register')
def register():
	# Serve the initial landing page. This comes from flask
	return render_template('register.html', 
			last_updated=lastUpdateTime('static/'))


@app.route('/details')
def details():
	# Serve the initial landing page. This comes from flask
	return render_template('status.html', 
			last_updated=lastUpdateTime('static/'))



if __name__ == '__main__':
	args = parseCommandLineArgs()
	app.run(host=args.hostIp, debug=args.debug)
