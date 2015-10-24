# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~
    A microblogging application written with Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
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
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

# initialize empty call list
callList = CallList()

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


#Use this to display calls
@app.route('/')
def public_timeline():
    """Displays the pending calls"""
    return render_template('layout.html', calls=callList.getCalls())


@app.route('/add_call', methods=['POST'])
def add_call():

    ## Take date input and change to python datetime
    call_date = datetime(*[int(v) for v in request.form['time_to_call'].replace('T', '-').replace(':', '-').split('-')])
    x=datetime.today()
    delta_t=call_date-x
    print(delta_t)
    secs=delta_t.seconds+1

    t = Timer(secs, make_call)
    t.start()


    """Registers a new pending call."""
    callList.appendCall(request.form['call_number'], call_date, request.form['call_content'])
    flash('Your call was recorded')
    return redirect(url_for('public_timeline'))

def make_call():
    name = 'myTest1'
    myTest = praw.Reddit(name.encode('utf-8'))
    theContent = myTest.get_front_page(limit = 1)
    theList = [x.title for x in theContent]
    # To find these visit https://www.twilio.com/user/account
    ACCOUNT_SID = ""
    AUTH_TOKEN = ""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(to="+1-787-461-0922", from_="+1-978-590-9760",
                           url="http://foo.com/call.xml")
    print(theList[0])


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime