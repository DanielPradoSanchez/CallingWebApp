# -*- coding: utf-8 -*-
"""
    A web app written with Flask and Twilio. The app allows
    you to call a phone and it automatically says the specified 
    name (Daniel Prado), and the title of the top content on
    Reddit at the time the call is made.
"""

import time
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack


from model import CallList


from twilio.rest import TwilioRestClient


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

ACCOUNT_SID = ""
AUTH_TOKEN = ""
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
callFromNumber = ""


@app.route('/')
def public_calls():
    """Displays the pending calls"""
    return render_template('layout.html', calls=callList.getCalls())


@app.route('/add_call', methods=['POST'])
def add_call():
    if (request.form['call_number'] and request.form['time_to_call']):
        callNumber = request.form['call_number']
        # Take date input and change to python datetime
        call_date = datetime(*[int(v) for v in request.form['time_to_call'].replace('T', '-').replace(':', '-').split('-')])
        time_of_request=datetime.today()
        delta_t=call_date-time_of_request
        secs=delta_t.seconds+1

        """Registers a new pending call."""
        if call_date > time_of_request:
            callList.appendCall(callNumber, call_date)
            t = Timer(secs, make_call(callNumber))
            t.start()
            flash('Your call was recorded')
        else:
            flash('Your call was not recorded. Please select some time in the future for your call to be made.')
    else:
        flash('Your call was not recorded. Please make sure all fields have an answer')
    return redirect(url_for('public_calls'))

def make_call(number_to_call):
    # To find these visit https://www.twilio.com/user/account
    call = client.calls.create(to=number_to_call, from_=callFromNumber,
                           url='https://sheltered-temple-5934.herokuapp.com/')