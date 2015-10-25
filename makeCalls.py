# -*- coding: utf-8 -*-
#
#   A web app written with Flask and Twilio. The app allows
#   you to call a phone and it automatically says the specified 
#   name (Daniel Prado), and the title of the top content on
#   Reddit at the time the call is made. The user is required to
#	input their authentication token, account SID, the number they
#	are calling from (a number associated with the account), the
#	number they are calling, and when the call is to be made (date and time)
#

#####
##### Change time stuff to UTC (get the time of today in utc)
#####

import time
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from model import CallList
from twilio.rest import TwilioRestClient
import twilio.twiml
from threading import Timer
import praw

# configuration
SECRET_KEY = 'development key'

# Creat the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

# initialize empty call list
callList = CallList()

myName = 'Daniel Prado'



@app.route('/')
def public_calls():
    """Displays the pending calls"""
    return render_template('layout.html', calls=callList.getCalls())


@app.route('/add_call', methods=['POST'])
def add_call():
	# Get inputs from form
	callNumber = request.form['call_number']
	callFrom = request.form['call_number_from']
	accountSid = request.form['account_sid']
	authToken = request.form['auth_token']
	timeToCall = request.form['time_to_call']

	allEntriesAnswered = (callNumber
						and callFrom 
						and accountSid 
						and authToken 
						and timeToCall)
    if (allEntriesAnswered):
        # Take date input and change to python datetime
        call_date = datetime(*[int(v) for v in request.form['time_to_call'].replace('T', '-').replace(':', '-').split('-')])
        
        time_of_request=datetime.today()
        

        # Determines if the time the call is to executed is in the future.
        # If the call is to be made in the future, the call goes through
        # and is placed on a pending/completed list of calls to be made.

        # This needs to be changed. Place this logic inside of make_call.
        if call_date > time_of_request:
        	# Finds the difference between the time the call was 
        	# registered and when it is to be executed.
        	delta_t=call_date-time_of_request
        	secs=delta_t.seconds+1


        	# Check if token and sid work
        	# look online for api (authentication checking)
        	# If that's not an option, look into python callbacks
        	# or try catch method

            callList.appendCall(callNumber, call_date)
            t = Timer(secs, make_call(callNumber))
            t.start()
            flash('Your call was recorded')
        else:
            flash('Your call was not recorded. Please select some time in the future for your call to be made.')
    else:
        flash('Your call was not recorded. Please make sure all fields have an answer')
    return redirect(url_for('public_calls'))

@app.route("/get_content", methods=['GET', 'POST'])
def hello():
	myTest = praw.Reddit('myTest1')
	topContent = myTest.get_front_page(limit = 1)
	listOfTopContentTitles = [x.title for x in topContent]
	topContentTitle = listOfTopContentTitles[0]
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say('My name is ' + myName)
    resp.say('The top content on Reddit right now is ' + topContentTitle)
    return str(resp)

def make_call(number_to_call):
    # To find these visit https://www.twilio.com/user/account
    print('got here')
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(to=number_to_call, from_=callFromNumber,
                           url='https://sheltered-temple-5934.herokuapp.com/')