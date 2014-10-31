from operator import attrgetter
import wykop
 
api = wykop.WykopAPI(appkey=MOTD_WYKOP_API_KEY, secretkey=MOTD_WYKOP_SECRET_KEY,
                         login=MOTD_WYKOP_LOGIN, accountkey=MOTD_WYKOP_ACCOUNT_KEY)
 
entries = api.tag("suchar")
items = entries['items']
best = max(items, key=attrgetter('vote_count') )
 
print best.body

