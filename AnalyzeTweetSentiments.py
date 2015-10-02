import codecs
import nltk
import pickle
f = open('classifier.pickle')
classifier = pickle.load(f)
f.close()
f = open('word_features.pickle')
word_features = pickle.load(f)
f.close()
print classifier.show_most_informative_features(100)

from pymongo import MongoClient
client = MongoClient()
db = client.tvshows
collection = db.tweets

def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def cleanup(word_list):
	clean_list = []
	for word in word_list:
		if(len(word) >=3 and word[0] != '#' and word[0] != '@' and 'http://' not in word and 'https://' not in word):
				clean_list = word
	return clean_list

def initial_analyzer(tweet):
	positive_emoticons = [':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D','=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)','<3']
	negative_emoticons = [':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',':c', ':{', '>:\\', ';(']
	positive_flag = False
	negative_flag = False
	for em in positive_emoticons:
		if(em in tweet):
			positive_flag = True
			break
	for em in negative_emoticons:
		if(em in tweet):
			negative_flag = True
			break
	if(negative_flag ^ positive_flag == False):
		return 'neutral'
	elif(negative_flag == True):
		return 'negative'
	else:
		return 'positive'

#tweetmap = []
count = 0
negative = 0
positive = 0
neutral = 0
#f = codecs.open('results.txt','w','utf-8')
for tweet_md in collection.find({"sentiment":{"$exists": False}},{"text":1, "id_str":1}):
	tweet = tweet_md['text']
	tweet_id = tweet_md['id_str']
	sentiment = initial_analyzer(tweet)
	if(sentiment == 'neutral'):
		Csentiment = classifier.classify(extract_features(tweet.split()))
		dist = classifier.prob_classify(extract_features(tweet.split()))
		if(Csentiment == 'n' and dist.prob('n') < 0.6):
			Csentiment = 'neutral'
		elif(Csentiment == 'n'):
			Csentiment = 'negative'
		else:
			Csentiment = 'positive'
		sentiment = Csentiment
	count = count + 1
	collection.update({"id_str":tweet_id}, {"$set":{"sentiment":sentiment}})
	print 'Processed ', count
	#print tweet, sentiment
	#print ('%d, %d, %d, %d') % (count,positive,neutral,negative)
	#tweetmap.append((tweet, sentiment))
	#if(sentiment == 'negative'):
	#	negative = negative + 1
	#elif(sentiment == 'neutral'):
	#	neutral = neutral + 1
	#else:
	#	positive = positive + 1
	#f.write(tweet + " " + sentiment + "\n")
#f.close()

print tweetmap