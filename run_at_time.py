from datetime import datetime
from threading import Timer
import praw
#import urllib3
#urllib3.disable_warnings()

x=datetime.today()
y=x.replace(day=x.day, hour=x.hour, minute=x.minute, second=x.second+2, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def get_Content():
    name = 'myTest1'
    myTest = praw.Reddit(name.encode('utf-8'))
    theContent = myTest.get_front_page(limit = 2)
    theList = [x.title for x in theContent]
    print(theList[0])

t = Timer(secs, get_Content)
t.start()