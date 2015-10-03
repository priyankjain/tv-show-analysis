from pymongo import MongoClient
client = MongoClient()
db = client.tvshows
collection = db.tweets
users = db.users

count = 0
SUIT_TAGS = ['#harveyspecter','@GabrielMacht','@halfadams', '#Suits', '#SuitsFinale','@Suits_USA']
for tweet in collection.find({"tvshow":{"$exists":False}},{"text":1,"id_str":1,"user_id_str":1}):
	text = tweet['text']
	id_str = tweet['id_str']
	user_id_str = tweet['user_id_str']
	tvshows = ""
	for tag in SUIT_TAGS:
		if(tag in text):
			tvshows = "suits"
			break

	if(tvshows == ""):
		for user in users.find({"id_str":user_id_str},{"screen_name":1}):
			name = user['screen_name']
			if(name in SUIT_TAGS):
				tvshows = "suits"
				break

	if(tvshows == ""):
		tvshows = "got"
	count = count + 1
	collection.update_one({"id_str":id_str},{"$set":{"tvshow":tvshows}})
	print count, text, tvshows
	#raw_input()