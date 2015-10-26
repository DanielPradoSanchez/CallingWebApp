#
#   A web app written with Flask and Twilio. The app allows
#   you to call a phone and it automatically says the specified 
#   name (Daniel Prado), and the title of the top content on
#   Reddit at the time the call is made. The user is required to
#	input their authentication token, account SID, the number they
#	are calling from (a number associated with the account), the
#	number they are calling, and when the call is to be made (date and time)
#

import time
from datetime import datetime
from datetime import timedelta
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from twilio.rest import TwilioRestClient
from threading import Timer
import praw

# configuration
SECRET_KEY = 'development key'

# Creat the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)


# Loads the web page
@app.route('/')
def public_calls():
	return render_template('layout.html')


# Handles registering a call
@app.route('/add_call', methods=['POST'])
def add_call():
	# Get inputs from form
	callNumber = request.form['call_number']
	callFrom = request.form['call_number_from']
	accountSid = request.form['account_sid']
	authToken = request.form['auth_token']
	timeToCall = request.form['time_to_call']

	# Check to see if any entries were left blank
	if (callNumber and callFrom and accountSid and authToken and timeToCall):
		# Take date input and change to python datetime
		callTimeLocal = datetime(*[int(v) for v in timeToCall.replace('T', '-').replace(':', '-').split('-')])

		timeOfRequestUTC=datetime.today()
		
		# Offset Eastern Standard Time to UTC
		callTimeUTC = timedelta(0,14400) + callTimeLocal

		# Make sure the requested time for the call to be made is in the future
		if callTimeUTC > timeOfRequestUTC:

			# Finds the difference between the time the call was 
			# registered and when it is to be executed.
			delta_t=callTimeUTC-timeOfRequestUTC
			secs=delta_t.total_seconds()

			# Sets up when the call is to be made
			Timer(secs, make_call,[callNumber, callFrom, accountSid,authToken]).start()
			flash('Your call has been recorded')
			
		else:
			flash('Your call was not recorded. Please select some time in the future for your call to be made.')
	else:
		flash('Your call was not recorded. Please make sure all fields have an answer')
	return redirect(url_for('public_calls'))

def make_call(numberToCall, callFromNumber, SID, token):
    # To find these visit https://www.twilio.com/user/account
	client = TwilioRestClient(SID, token)
	# The url field here leads to another web app (SpeechForCallingWebApp)
	call = client.calls.create(to=numberToCall, from_=callFromNumber, url='https://sheltered-temple-5934.herokuapp.com/')