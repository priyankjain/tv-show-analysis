import math
from genderizer.genderizer import Genderizer
import sexmachine.detector as gender
d = gender.Detector()
from genderize import Genderize

from pymongo import MongoClient
client = MongoClient()
db = client.tvshows
collection = db.users

tweets = db.tweets
count = 0
for user_md in collection.find({"gender":{"$exists":False}},{"name":1, "description":1,"id_str":1}):
		name = user_md['name']
		description = user_md['description']
		id_str = user_md['id_str']
		user_gender = ''
		user_gender = d.get_gender(name)
		if(user_gender == 'andy'):
			try:
				if(description != ''):
					user_gender = Genderizer.detect(firstName = name, text = description)
			except ZeroDivisionError:
				user_gender = 'None'
			if(user_gender == 'None'):
				for user_tweets in tweets.find({"user_id_str":id_str},{"text":1}).limit(10):
					twt = user_tweets['text']
					try:
						user_gender = Genderizer.detect(firstName = name, text = twt)
						if(user_gender != 'None'):	
							break
					except ZeroDivisionError:
						user_gender = 'None'
			if(user_gender == 'None'):
				list = []
				list.append(name)
				response_list = Genderize().get(list)
				if(len(response_list) > 0):
					user_gender = response_list[0]['gender']
		collection.update({"id_str":id_str}, {"$set":{"gender":user_gender}})
		count = count + 1
		print 'Processed', count

