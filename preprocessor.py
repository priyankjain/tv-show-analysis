import pymongo
import string
from pymongo import MongoClient
client = MongoClient();
db = client.tvshows
collection = db.rawtweets
destTweets = db.tweets
destUsers = db.users
for tweet in collection.find():
	if (destTweets.count({"id_str":tweet['id_str']}) == 0):
		destTweet = {}
		destTweet['id_str']=tweet['id_str']
		lindex = string.find(tweet['source'],'>')+1
		rindex = string.rfind(tweet['source'],'<')
		if(rindex == -1):
			rindex = len(tweet['source'])
		destTweet['source']=tweet['source'][lindex:rindex]
		destTweet['user_id_str']=tweet['user']['id_str']
		destTweet['favorite_count']=tweet['favorite_count']
		destTweet['lang']=tweet['lang']
		destTweet['retweet_count']=tweet['retweet_count']
		destTweet['text']=tweet['text']
		destUser = {}
		destUser['id_str']=tweet['user']['id_str']
		destUser['description']=tweet['user']['description']
		destUser['followers_count']=tweet['user']['followers_count']
		destUser['lang']=tweet['user']['lang']
		destUser['name']=tweet['user']['name']
		destUser['screen_name']=tweet['user']['screen_name']
		destTweets.insert(destTweet)
		if(destUsers.count({"id_str":destUser['id_str']}) == 0):
			destUsers.insert(destUser)
