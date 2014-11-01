#!/usr/bin/python

#############################################################################
# Skrypt: mirkoAsMOTD
# autor: @noisy
# wersja: 0.0.8

MOTD_WYKOP_API_KEY = ''
MOTD_WYKOP_SECRET_KEY = ''
MOTD_WYKOP_LOGIN = ''
MOTD_WYKOP_ACCOUNT_KEY = ''

MOTD_WYKOP_TAG = 'suchar'

#############################################################################

from operator import attrgetter
from termcolor import colored
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
item.body = re.sub('#<a href=\"#(\w+)\">\w+</a>', colored('#', 'blue', attrs=['bold']) + colored('\g<1>', 'white', attrs=['bold']), item.body)


# extract and color links
g = re.findall('<a href="(.*)" rel="nofollow">(.*)</a>', item.body, re.MULTILINE)
links = ''
for i, (link, opis) in enumerate(g):
    item.body = re.sub(
        '<a href="%s" rel="nofollow">%s</a>' % (link, opis),
        (colored('%s', 'white', attrs=['bold']) + colored('[%d]', 'yellow', attrs=['bold'])) % (opis, i+1),
        item.body
    )

    links += (colored('[%d]', 'yellow', attrs=['bold']) + ' - %s \n') % (i+1, link)


# get and set nick color
author_profile = api.get_profile(item.author)

author_colors = {
    # 0	Zielony
    # 1	Pomaranczowy
    # 2	Bordowy
    # 5	Administrator
    # 1001	Zbanowany
    # 1002	Usuniety
    # 2001	Klient

    0: 'green',
    1: 'yellow',
    2: 'red',
    5: 'magenta',
    1001: 'white',
    1002: 'white',
    2001: 'blue',
}

print ("""
%(votes_color_scheme)s %(author_color_scheme)s

%(body_color_scheme)s

%(links)s
""" % {
    'author_color_scheme': '- @' + colored('%(author)s', author_colors[author_profile.author_group]) + '',
    'votes_color_scheme': colored('[', 'white', attrs=['bold']) + colored('+%(votes)s', 'green', attrs=['bold']) + colored(']', 'white', attrs=['bold']),
    'body_color_scheme': '%(body)s',
    'links': '%(links)s',
}) % {
    'author': item.author,
    'votes': item.vote_count,
    'body': item.body,
    'links': links,
}
