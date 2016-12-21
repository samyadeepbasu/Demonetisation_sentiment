############################################ Script to analyse the Post Demonetisation scenario presently ###################################################
#############################################################################################################################################################
#############################################################################################################################################################

import json
import pandas as pd 
import matplotlib.pyplot as plt 
import re
from operator import itemgetter
from nltk.tokenize import sent_tokenize
import math

tweets_data_path = 'twitter_data.txt'

tweets_data = []

tweets_file = open(tweets_data_path,"r")


for line in tweets_file:
	try:
		#Conversion of the tweets into JSON Format
		tweet = json.loads(line)
		#Appending the twitter feed data into a list
		tweets_data.append(tweet)
	except:
		continue


#Storing the Tweets in a list
tweets = []
location = []
for tweet in tweets_data:
	try:
		tweets.append(tweet['text'])
		if tweet['place']!=None:
			location.append(tweet['place']['full_name'])

	except:
		continue


number_of_tweets = len(tweets)
number_of_unique_tweets = len(set(tweets))

unique_tweets = set(tweets)
unique_location = set(location)

location_count = {}

#Location count metric for the origin of the tweet
for loc in unique_location:
	location_count[loc] = location.count(loc)

# Printing the location from where most of the tweets about Demonetisation were made
#print sorted(location_count.items(),key=itemgetter(1),reverse=True)


#### Pre-processing ###

#Converting tweets to lower_case 
unique_tweets = [x.lower() for x in unique_tweets]

#Extracting keywords from the tweets

keywords = []

for tweet in unique_tweets:
	temp = tweet.split()
	for i in temp:
		keywords.append(i)



unique_words = set(keywords)

#print len(unique_words)
#print len(keywords)

#Occurrence of major words
word_dict = {}

for word in unique_words:
	word_dict[word] = keywords.count(word)


word_dict = sorted(word_dict.items(),key=itemgetter(1),reverse=True)

#print word_dict


j = 0
top_50 = []

#Top 30 words without Filters 
for item in word_dict:
	top_50.append(item[0])
	if j==50:
		break

	j = j + 1



#print top_30

######################################################### Unsupervised Classification of Tweets ###########################################################
###########################################################################################################################################################

# This is done using Pointwise Mutation Information wrt to a positive vocabulary and negative vocabulary


#Construction of the vocabulary

#Positive word list construction
pos = open('positive-words.txt','r')
positive_words = []
for line in pos:
	positive_words.append(line[:len(line)-1])



#Negative Word List construction
neg = open('negative-words.txt','r')
negative_words = []
for line in neg:
	negative_words.append(line[:len(line)-1])


sentiment_dict = {} 

#Total number of Tweets
total_tweets = len(unique_tweets)

#Function to find the document frequency - Number of documents which contain the required term
def find_doc_frequency(term):
	count = 0
	for tweet in unique_tweets:
		if term in tweet.split():
			count = count + 1


	return count 


def combined_doc_frequency(term1,term2):
	count = 0
	for tweet in unique_tweets:
		if term1 in tweet.split() and term2 in tweet.split():
			count = count + 1

	return count


#Doc frequency of positive and negative words 
positive_doc_frequency = {}
negative_doc_frequency = {}

#Positive Words and their corresponding document frequencies
for word in positive_words:
	positive_doc_frequency[word] = find_doc_frequency(word)

#Negative Words and their corresponding document frequencies
for word in negative_words:
	negative_doc_frequency[word] = find_doc_frequency(word)


#print positive_doc_frequency

# Each tweet will be now labelled as positive or negative through sentiment analysis
for tweet in unique_tweets:
	#Splitting the tweet into words
	temp = tweet.split()
	#For each word the Semantic Orientation will be found
	SO = 0
	for word in temp:
		#Document frequency for the word
		doc_freq_1 = find_doc_frequency(word)
		PMI_positive = 0
		PMI_negative = 0
		for pos_word in positive_words:
			#Document frequency when both occur together
			combined_frequency = combined_doc_frequency(word,pos_word)
			#Calculating the PMI
			if combined_frequency == 0:
				PMI_positive = 0
			else:
			    PMI_positive = PMI_positive + math.log(float(combined_frequency * len(unique_tweets)) / float(positive_doc_frequency[pos_word] * doc_freq_1))

		for neg_word in negative_words:
			#Document frequency when both occur together
			combined_frequency = combined_doc_frequency(word,neg_word)
			#Calculating the PMI
			if combined_frequency ==0:
				PMI_negative = 0
			else:
			    PMI_negative = PMI_negative + math.log(float(combined_frequency * len(unique_tweets)) / float(negative_doc_frequency[neg_word] * doc_freq_1))

		PMI_net = PMI_positive - PMI_negative
		SO = SO + PMI_net

	sentiment_dict[tweet] = SO










		






