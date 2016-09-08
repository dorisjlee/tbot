from time import sleep
from secrets import *
import tweepy
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
dic={}
f = open("id_topic","r")
for i in f.readlines():
    item = i.split(',')
    dic[int(item[0])]=item[1][:-1].lower()
replied = []
while (True):
	try:
		all_reply = api.search(q="@guessthewiki")
	except(tweepy.error.RateLimitError):
		print "Search Rate Limit Error"
		sleep(100)
	print len(all_reply)
	for reply in all_reply:
	    guess = reply.text[20:-1].lower()
	    if reply.text[:20]=='@guessthewiki Is it ' and reply.id not in replied:
	    	try:
		    	print "New reply guess: ", guess
		        if dic[reply.in_reply_to_status_id] == guess:
		            api.update_status("@{} Good job! That's correct!".format(reply.user.screen_name),reply.id)
		        elif guess in dic[reply.in_reply_to_status_id] :
		            api.update_status("@{} Very close!!".format(reply.user.screen_name),reply.id)
		        else:
		            api.update_status("@{} Try again!!".format(reply.user.screen_name),reply.id)
	    	except(tweepy.error.TweepError):
				print "Skip: Duplicate Status"
				if reply.id not in replied:  replied.append(reply.id)
		sleep(10)
		#Keep track of which tweet is already replied
		if reply.id not in replied: replied.append(reply.id)
	