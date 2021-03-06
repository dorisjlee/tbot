import time 
import os
from time import gmtime, strftime
from secrets import *
import tweepy
import wikipedia
from wordcloud import WordCloud
from pyshorteners import Shortener
logfile_name = "tweets_doris.log"
def do_cool_stuff():
        text=""
        # Trying to find wikipedia pages that have a lot of words so that the wordcloud looks pretty.
        while(len(text)<500):
            topic = wikipedia.random()
            print "trying: ", topic
            try:
	        text = wikipedia.summary(topic)
	    except(wikipedia.exceptions.DisambiguationError):
	        continue
	#Generate and Save WordCloud
	wc = WordCloud(max_font_size=40, relative_scaling=.5)
	wc.generate(text)
	image = wc.to_image()
	image.save("../images/"+topic+".png")
	fn = os.path.abspath("../images/"+topic+".png")
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)
	url = 'https://en.wikipedia.org/wiki/{}'.format(topic.replace (" ", "_"))
	shortener = Shortener('Tinyurl')

	# Send the tweet and log success or failure
	try:
	#    api.update_with_media(fn,status="Wordcloud of Wikipedia Article Summary of "+topic+"."+shortener.short(url))
	    status  = api.update_with_media(fn)
	    #Storing the Tweet ID and Topic
	    f = open("id_topic","a")
	    f.write(str(status.id) +","+topic+"\n")
	    f.close()
	except tweepy.error.TweepError as e:
	    log(e.message)
	else:
	    log("Tweeted: " + topic)
def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)
for i in range(50):
    print "sleeping "
    time.sleep(10)
    print i ,"th tweet"
    do_cool_stuff()
