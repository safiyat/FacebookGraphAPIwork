from flask import Flask, redirect, request
import requests

import oauth2client.client as oc

APP_ID = 'API_ID'
APP_SECRET = 'API_SECRET'
APP_NAME = 'EmailID Chor'
REDIRECT_URI = 'http://localhost:8080/fapicallback'

app = Flask(__name__)
credentials = None
@app.route('/')
def hello_world():
	return redirect('/login')


@app.route('/login')
def login():

	auth_uri = 'https://www.facebook.com/dialog/oauth?client_id=' + APP_ID + '&redirect_uri=' + REDIRECT_URI
	print auth_uri
	return redirect(auth_uri)

@app.route('/fapicallback')
def check_login():
	error = request.args.get('error')
	if error is not None:
		return 'invalid login'
	code = request.args.get('code')
	req = 'https://graph.facebook.com/oauth/access_token?client_id=' + APP_ID + '&redirect_uri=' + REDIRECT_URI + '&client_secret=' + APP_SECRET + '&code=' + code
	print '>>>>>>>>>>>>>>>> Req: %s' % req
	response = requests.get(req).content
	if response.startswith('access_token'):
		start = 13
		end = response.find('expires', start) - 1
		access_token = response[start:end]
		"""
		print '>>>>>>>>>>>>>>>> AT: %s' % access_token
		print '>>>>>>>>>>>>>>>> %s' % response
		temp = access_token + '\n' + response[13:]
		"""
		req = 'https://graph.facebook.com//v2.2/me/friends?fields=name&access_token=' + access_token
		temp = requests.get(req).content
		return temp
	else:
		return 'Error'


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=8080)
