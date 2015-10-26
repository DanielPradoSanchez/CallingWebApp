# MakeCallsWebApp

I put a few more hours of work into this because I thought it would be fun to get something online and have a small web app.

Required Libraries:
Python Standard Library
Flask
gunicorn
itsdangerous
MarkUpSafe
requests
six
Twilio
update-checker
wheel

Installing:
Nothing needs to be installed to make the call (everything is in the web app)

Make A Call:
Go to http://pradosan-twilcall.herokuapp.com/. From here you can input the number you are going to call (+1-...-...-...), the number you are calling from which needs to be associated with the account (+1-...-...-...), the SID associated with the account, the authentication token associated with the account, and then you can select a date and time for the call to be made in the future. If any of the fields are left blank or the time selected is in the past, the web app will not allow you to make the call (it will not crash). If the information dealing with the account are incorrect (SID, token, phone number), the app will lead to a crashed page. If this happens you can go back to http://pradosan-twilcall.herokuapp.com/ and try to make the call again.

The call wil say: My name is Daniel Prado. The top content on Reddit right now is (and the title of the top content on the front page of Reddit). This is dictated by the web app at https://sheltered-temple-5934.herokuapp.com/. I set this up in order for twilio to read the xml of the page.


Git pulls:
The pull request for the calling web app is at: https://github.com/DanielPradoSanchez/theTest/pull/1

The pull request for the web app that dictates what the call will say is at: 
