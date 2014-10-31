#!/usr/bin/python

#############################################################################
# Skrypt: mirkoAsMOTD
# autor: @noisy
# wersja: 0.0.6

MOTD_WYKOP_API_KEY = ''
MOTD_WYKOP_SECRET_KEY = ''
MOTD_WYKOP_LOGIN = ''
MOTD_WYKOP_ACCOUNT_KEY = ''

MOTD_WYKOP_TAG = 'suchar'

#############################################################################

from operator import attrgetter
import wykop
import re

from datetime import datetime, timedelta

api = wykop.WykopAPI(
    appkey=MOTD_WYKOP_API_KEY,
    secretkey=MOTD_WYKOP_SECRET_KEY,
    login=MOTD_WYKOP_LOGIN,
    accountkey=MOTD_WYKOP_ACCOUNT_KEY
)

day_ago = datetime.now() - timedelta(hours=24)

page = 0
entries = api.tag(MOTD_WYKOP_TAG, page)
latest_datetime = entries['items'][-1].date

# fetch more if needed
while datetime.strptime(latest_datetime, "%Y-%m-%d %H:%M:%S") > day_ago:
    page += 1
    entries['items'] += api.tag(MOTD_WYKOP_TAG, page)['items']
    latest_datetime = entries['items'][-1].date

# filter if too much
entries['items'] = [
    item
    for item in entries['items']
    if datetime.strptime(item.date, "%Y-%m-%d %H:%M:%S") > day_ago
]

# find the most popular
item = max(entries['items'], key=attrgetter('vote_count'))

# remove html new lines and links from tags
item.body = item.body.replace('<br />', '')
item.body = re.sub('<a href=\"#(\w+)\">\w+</a>', '\g<1>', item.body)

print item.body
