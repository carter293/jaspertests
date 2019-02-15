import httplib2
import random
import sys
import datetime
import re
import gflags

from client.app_utils import getTimezone
from dateutil import tz
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import *

# Written by Marc Poul Joseph Laventure

FLAGS = gflags.FLAGS
WORDS = ["Calendar", "Events", "Check", "My"]
client_id = '838713519247-e8ruaheudf81d1jv4tjdfa9gla6ak39t.apps.googleusercontent.com'
client_secret = 'Y0DUWPvLF9BsLMgi13nllWPM'

monthDict = {'January': '01',
             'February': '02',
             'March': '03',
             'April': '04',
             'May': '05',
             'June': '06',
             'July': '07',
             'August': '08',
             'September': '09',
             'October': '10',
             'November': '11',
             'December': '12'}

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

if bool(re.search('--noauth_local_webserver', str(sys.argv), re.IGNORECASE)):
    argv = FLAGS(sys.argv[1])


def getEventsToday(profile, mic):
    tz = getTimezone(profile)

    # Get Present Start Time and End Time in RFC3339 Format
    d = datetime.datetime.now(tz=tz)
    utcString = d.isoformat()
    m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
    utcString = str(m.group(0))
    todayStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
    todayEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString
    page_token = None
    x = 0
    GCIntros = ["ah ok so Matt for your google calendar you have",
                "Matt your google calendar is telling me that you have",
                "Today your google calendar has for you",
                "Ok today we have on your google calendar"
                "ah ok so Carter for your google calendar you have",
                "Carter your google calendar is telling me that you have",]
    FCIntros = ["and for your facebook calendar tomorrow you have",
                "your facebook calendar also is telling me that tomorrow you have",
                " and tomorrow your facebook calendar has for you",
                ".. Ok tomorrow we also have on your facebook calendar",
                "and for your facebook calendar tomorrow you have",
                "also your facebook calendar is telling me that tomorrow you have"]
    EmptyResponses = ["sink a couple cold ones champ",
                "hit the library loser",
                "please look at my code I feel like poo",
                "maybe lay of the tav",
                "hit the bread water cuck", 
                "grab a cold on champ",
                "hit the books loser",
                "please tweak me I feel like shit",
                "maybe lay of the beers",
                "hit the beers pussy"]
    GCIntro = random.choice(GCIntros)
    mic.say(GCIntro)


    while True:

        # Gets events from primary calender from each page in present day boundaries
        events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=todayStartTime,
                                       timeMax=todayEndTime).execute()

        if (len(events['items']) == 0):
            mic.say("no events scheduled")
            x += 1
            break

        for event in events['items']:

            try:
                eventTitle = event['summary']
                eventTitle = str(eventTitle)
                eventRawStartTime = event['start']
                eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                temp = eventRawStartTime[1]
                startHour, startMinute, temp = temp.split(":", 2)
                startHour = int(startHour)
                appendingTime = "am"

                if ((startHour - 12) > 0):
                    startHour = startHour - 12
                    appendingTime = "pm"

                startMinute = str(startMinute)
                startHour = str(startHour)
                mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime)  # This will be mic.say

            except KeyError, e:
                mic.say("Check Calender that you added it correctly")

        page_token = events.get('nextPageToken')

        if not page_token:
            break

    FCIntro = random.choice(FCIntros)
    mic.say(FCIntro)

    while True:

        # Gets events from primary calender from each page in present day boundaries
        events = service.events().list(calendarId='muoqenhe7pqvh6eu9t96tnl0mrma6g2h@import.calendar.google.com',
                                       pageToken=page_token, timeMin=todayStartTime,
                                       timeMax=todayEndTime).execute()

        if (len(events['items']) == 0):
            mic.say("no events scheduled")
            if x == 1: 
                EmptyResponse = random.choice(EmptyResponses)
                mic.say(EmptyResponse)
            return

        for event in events['items']:

            try:
                eventTitle = event['summary']
                eventTitle = str(eventTitle)
                eventRawStartTime = event['start']
                eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                temp = eventRawStartTime[1]
                startHour, startMinute, temp = temp.split(":", 2)
                startHour = int(startHour)
                appendingTime = "am"

                if ((startHour - 12) > 0):
                    startHour = startHour - 12
                    appendingTime = "pm"

                startMinute = str(startMinute)
                startHour = str(startHour)
                mic.say(
                    eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime)  # This will be mic.say

            except KeyError, e:
                mic.say("Check Calender that you added it correctly")

        page_token = events.get('nextPageToken')

        if not page_token:
            return


def getEventsTomorrow(profile, mic):
    # Time Delta function for adding one day

    one_day = datetime.timedelta(days=1)
    tz = getTimezone(profile)

    # Gets tomorrows Start and End Time in RFC3339 Format

    d = datetime.datetime.now(tz=tz) + one_day
    utcString = d.isoformat()
    m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
    utcString = m.group(0)
    tomorrowStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
    tomorrowEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString

    page_token = None

    GCIntros = ["Alrighty so Matty for your google calendar tomorrow you have",
                "Matt your google calendar is telling me that tomorrow you have",
                "Tomorrow your google calendar has for you",
                "Ok tomorrow we have on your google calendar",
                "Alrighty so Carter for your google calendar tomorrow you have",
                "Carter your google calendar is telling me that tomorrow you have"]
    FCIntros = ["and for your facebook calendar tomorrow you have",
                "your facebook calendar also is telling me that tomorrow you have",
                " and tomorrow your facebook calendar has for you",
                ".. Ok tomorrow we also have on your facebook calendar",
                "and for your facebook calendar tomorrow you have",
                "also your facebook calendar is telling me that tomorrow you have"]
    GCIntro = random.choice(GCIntros)
    mic.say(GCIntro)

    while True:

        # Gets events from primary calender from each page in tomorrow day boundaries

        events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=tomorrowStartTime,
                                       timeMax=tomorrowEndTime).execute()
        if (len(events['items']) == 0):
            mic.say("no events scheduled")
            x += 1
            break

        for event in events['items']:

            try:
                eventTitle = event['summary']
                eventTitle = str(eventTitle)
                eventRawStartTime = event['start']
                eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                temp = eventRawStartTime[1]
                startHour, startMinute, temp = temp.split(":", 2)
                startHour = int(startHour)
                appendingTime = "am"

                if ((startHour - 12) > 0):
                    startHour = startHour - 12
                    appendingTime = "pm"

                startMinute = str(startMinute)
                startHour = str(startHour)
                mic.say(
                    eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime)  # This will be mic.say

            except KeyError, e:
                mic.say("Check Calender that you added it correctly")

        page_token = events.get('nextPageToken')

        if not page_token:
            break


    FCIntro = random.choice(FCIntros)
    mic.say(FCIntro)

    while True:

        # Gets events from primary calender from each page in tomorrow day boundaries

        events = service.events().list(calendarId='muoqenhe7pqvh6eu9t96tnl0mrma6g2h@import.calendar.google.com', pageToken=page_token, timeMin=tomorrowStartTime,
                                       timeMax=tomorrowEndTime).execute()
        if (len(events['items']) == 0):
            mic.say("nothing scheduled")
            if x == 1: 
                EmptyResponse = random.choice(EmptyResponses)
                mic.say(EmptyResponse)
            return

        for event in events['items']:

            try:
                eventTitle = event['summary']
                eventTitle = str(eventTitle)
                eventRawStartTime = event['start']
                eventRawStartTime = eventRawStartTime['dateTime'].split("T")
                temp = eventRawStartTime[1]
                startHour, startMinute, temp = temp.split(":", 2)
                startHour = int(startHour)
                appendingTime = "am"

                if ((startHour - 12) > 0):
                    startHour = startHour - 12
                    appendingTime = "pm"

                startMinute = str(startMinute)
                startHour = str(startHour)
                mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime)  # This will be mic.say

            except KeyError, e:
                mic.say("Check Calender that you added it correctly")

        page_token = events.get('nextPageToken')

        if not page_token:
            return


# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.

flow = OAuth2WebServerFlow(client_id, client_secret, scope)

# Create a Storage object. This object holds the credentials that your
# application needs to authorize access to the user's data. The name of the
# credentials file is provided. If the file does not exist, it is
# created. This object can only hold credentials for a single user, so
# as-written, this script can only handle a single user.
storage = Storage('credentials.dat')

# The get() function returns the credentials for the Storage object. If no
# credentials were found, None is returned.
credentials = storage.get()

# If no credentials are found or the credentials are invalid due to
# expiration, new credentials need to be obtained from the authorization
# server. The oauth2client.tools.run_flow() function attempts to open an
# authorization server page in your default web browser. The server
# asks the user to grant your application access to the user's data.
# If the user grants access, the run_flow() function returns new credentials.
# The new credentials are also stored in the supplied Storage object,
# which updates the credentials.dat file.
if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

# Create an httplib2.Http object to handle our HTTP requests, and authorize it
# using the credentials.authorize() function.
http = httplib2.Http()

http = credentials.authorize(http)

# The apiclient.discovery.build() function returns an instance of an API service
# object can be used to make API calls. The object is constructed with
# methods specific to the calendar API. The arguments provided are:
#   name of the API ('calendar')
#   version of the API you are using ('v3')
#   authorized httplib2.Http() object that can be used for API calls
service = build('calendar', 'v3', http=http)


def handle(text, mic, profile):

    if bool(re.search('Today', text, re.IGNORECASE)):
        getEventsToday(profile, mic)

    if bool(re.search('Tomorrow', text, re.IGNORECASE)):
        getEventsTomorrow(profile, mic)


def isValid(text):
    return bool(re.search(r'\bCalendar\b', text, re.IGNORECASE))
