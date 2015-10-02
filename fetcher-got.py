from TwitterSearch import *
import logging
import json
import pymongo
import time
from pymongo import MongoClient
client = MongoClient()
db = client.tvshows
collection = db.rawtweets
logging.basicConfig(filename='fetcher.log',level=logging.DEBUG)
try:

	tso = TwitterSearchOrder()
	tso.set_keywords(['game of thrones', '#GoT', '#GameofThrones','@GameOfThrones'], or_operator = True)
#	tso.set_language('en')
#	tso.set_include_entities(False)
	
	ts = TwitterSearch('I3VcDP6wBv8KmwP0ZGV07yTAX','T4ST3R2M4vVVpa8EdvBFwhuE6IPtBJBnggOmr1Nsf5tkIVBypt','472194816-mPhURi7SFByyPMxPnOjfJ0UuDmhPJkdEGt6GgGx2','grQCemkXxuBfWm4IOtrrU6vbsm6On0LDVYtpuhzsp1UFl')
	logging.info("Initialized twitter objects, now querying...")
	def rate_limit_check(current_ts_instance):
		queries, tweets_seen = current_ts_instance.get_statistics()
		logging.info("Doing query number {0:d} in current window".format(queries+1))
		logging.info("Sleeping for 2 seconds now")
		time.sleep(2)
		logging.info("Sleeping time over")
		queries=queries%180

	for tweet in ts.search_tweets_iterable(tso, callback=rate_limit_check):
		global collection
		print collection.count({"id_str":tweet['id_str']})
		if(collection.count({"id_str":tweet['id_str']}) == 0):
			collection.insert_one(tweet)

	logging.info("Program completed successfully. Exiting.")

except TwitterSearchException as e:
	logging.error(e)
