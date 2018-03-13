# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com

import tweepy
import re
import nltk
import string
import mongo
import pandas as pd
import nltk.tag.stanford as st


from time import sleep
from tweepy import OAuthHandler
from collections import Counter
from nltk.corpus import stopwords
from collections import defaultdict

''' preprocessing for tokenizing is done using information from the following source ::
   https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/'''

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""


regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r'(?:&[\w_]+)', #&-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    # r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)



class TwitterDataCollection():
    def __init__(self):

        self.consumer_key = 'XXXXXXXXXXXXXXX'
        self.consumer_secret = 'XXXXXXXXXXXXXXXXX'
        self.access_token = 'XXXXXXXXXXXXXXXXXX'
        self.access_secret = 'XXXXXXXXXXXXXXXXXXX'
        self.tweetLimit = 10000

    def getAPIHandle(self):

        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        return tweepy.API(auth)

    def fetchTweetsAndStore(self, collection):

        tweetsCount = 0
        lastId = -1
        maxTweets = 10000

        api = self.getAPIHandle()

        while tweetsCount < maxTweets:

            count = maxTweets - tweetsCount
            try:
                tweetSet = api.search(q = ('a'),
                                      count = count,
                                      max_id=str(lastId - 1),
                                      tweet_mode = 'extended',
                                      lang = 'en')
                # print(len(tweetSet))

                if not tweetSet:
                    break

                tweets = []
                for t in tweetSet:
                    if t._json['place'] is not None and t._json['created_at'] is not None:
                        tweets.append(t)

                tweetsCount += len(tweets)

                lastId = tweetSet[-1].id

                for tweet in tweets:
                    jsonTweet = tweet._json

                    mongo.dataBase[collection].insert_one(jsonTweet)

            except tweepy.TweepError as err:
                sleep(60 * 15)

class ProcessDataForNamedEntities():

    def __init__(self):
        self.data = None
        self.stopWords = self.stopWordCollection()

    def fetchData(self, collection):
        self.data = mongo.dataBase[collection].find({})

    def stopWordCollection(self):
        punctuation = list(string.punctuation)
        firstLetterCapital = [string.capwords(word) for word in
                              (stopwords.words(['english', 'french', 'spanish']))]

        stopTerms = stopwords.words(['english', 'french', 'spanish']) + punctuation + ['RT', 'via', 'U', 'La', 'El',
                                                                                       'Le', 'Un', "I'm", "I'll"] + firstLetterCapital

        return stopTerms

    def tokenize(self, sentence):
        return tokens_re.findall(sentence)

    def preProcess(self, sentence, lowercase=False):
        tokens = self.tokenize(sentence)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def filterData(self, frequentTermFlag):

        pronounTermList = []
        filteredListCollection = []

        if frequentTermFlag is True:
            index = 'full_text'
        else:
            index = 'summary'


        for record in self.data.limit(10000):
            prevTag = None

            allTerms = [term for term in self.preProcess(record[index]) if term not in self.stopWords]

            filteredList = []
            for term in allTerms:
                if not term.startswith('https') | term.startswith('@') | term.startswith('#') | term.startswith('&'):
                    filteredList.append(term)

            filteredListCollection.append(filteredList)
            if frequentTermFlag is True:
                entityTags = nltk.pos_tag(filteredList)

                for tag in entityTags:

                    if tag[1] == 'NNP' and prevTag == 'NNP':
                        pronounTermList[-1] = pronounTermList[-1] + str(' ') + str(tag[0])
                    else:
                        pronounTermList.append(tag[0])

                    prevTag = tag[1]

        return pronounTermList, filteredListCollection

    def getNamedEntities(self, **kwargs):

        countTerms = Counter()
        pronounTermList, filteredListCollection  = self.filterData(kwargs['FrequentTerms'])

        if kwargs['FrequentTerms'] is True:
            taggerHandle = st.StanfordNERTagger(
                '/home/harsh/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                '/home/harsh/stanford-ner-2014-06-16/stanford-ner.jar')

            entityList = taggerHandle.tag(pronounTermList)
            finalEntityList = [term[0] for term in entityList if not term[1] == 'O']
            countTerms.update(finalEntityList)
            frequentWords = countTerms.most_common(5)
            # print(frequentWords)
            return frequentWords, filteredListCollection
        else:
            return filteredListCollection

    def fetchDataForAnalysis(self, frequentWords, entityList, **kwargs):
        pd.set_option('display.max_colwidth', -1)

        dataFrame = pd.DataFrame(list(self.data))
        dates = defaultdict(list)
        locations = defaultdict(list)
        phrases = defaultdict(list)
        if kwargs['Source'] == 'Twitter':

            for word in frequentWords:
                rows = dataFrame[dataFrame['full_text'].str.contains(str(' ' + word[0] + ' ')) == True]

                for date in rows['created_at']:
                    dates[word[0]].append(date)

                for loc in rows['place']:
                    if loc is not None:
                        try:
                            locations[word[0]].append(loc['country_code'])
                        except KeyError:
                            pass

        else:
            for word in frequentWords:
                rows = dataFrame[dataFrame['summary'].str.contains(str(' ' + word[0] + ' ')) == True]
                for date in rows['published_at']:
                    dates[word[0]].append(date)

                for loc in rows['source']:
                    locations[word[0]].append(loc)


        for w in frequentWords:
            for phrase in entityList:
                if w[0] in phrase:
                    phrases[w[0]].append(phrase)

        return dates, locations, phrases
