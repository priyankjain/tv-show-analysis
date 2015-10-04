import json
import re
import nltk
import sys
import pickle
# Load positive tweets
labelled_tweets = []

def isIncluded(e):
	if(e[0] == '#' or e[0] == '@'):
		return False
	if("http://" in e or "https://" in e):
		return False
	return True

with open('/home/anonymous/Desktop/Downloads/twitter_samples/positive_tweets.json','r') as f:
	for line in f:
			rawtweet = json.loads(line)
			labelled_tweets.append((rawtweet['text'],'p'))

with open('/home/anonymous/Desktop/Downloads/twitter_samples/negative_tweets.json','r') as f:
	for line in f:
			rawtweet = json.loads(line)
			labelled_tweets.append((rawtweet['text'],'n'))

tweets = []
for (words, sentiment) in labelled_tweets:
	words_filtered = [re.sub(r'[^\w\s]','',e).lower() for e in words.split() if len(re.sub(r'[^\w\s]','',e))>=3 and isIncluded(e)]
	tweets.append((words_filtered, sentiment))	

def get_words_in_tweets(tweets):
	all_Words = []
	for (words, sentiment) in tweets:
		all_Words.extend(words)
	return all_Words

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features


training_set = nltk.classify.apply_features(extract_features, tweets)

print training_set
print 'Training set prepared, training the classifier now'
classifier = nltk.NaiveBayesClassifier.train(training_set)
print 'Training completed'
print classifier.show_most_informative_features(32)

f = open('classifier.pickle','wb')
pickle.dump(classifier,f)
f.close()

f = open('word_features.pickle','wb')
pickle.dump(word_features, f)
f.close()