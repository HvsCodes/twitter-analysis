# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com


import graphs
import pycountry
from time import sleep
from textblob import TextBlob
from collections import defaultdict

class Analysis():
    def __init__(self, commonEntities):
        self.tweetSentiment = {}
        self.tweetContent = {}
        self.tweetTemporal = {}
        self.tweetSpatial = {}
        self.newsSentiment = {}
        self.newsContent = {}
        self.newsTemporal = {}
        self.newsSpatial = {}
        self.commonEntities = commonEntities

    def plotGraph(self):


        for entity in self.commonEntities:
            e = entity[0]
            graphs.temporalGraphs(self.tweetTemporal[e], self.newsTemporal[e], e)
            sleep(2)
            graphs.sentimentGraph(self.tweetSentiment[e], self.newsSentiment[e], e)
            sleep(2)
            graphs.contentGraph(self.tweetContent[e], self.newsContent[e], e)
            sleep(2)
            graphs.spatialGraph(self.tweetSpatial[e], self.newsSpatial[e], e)
            sleep(2)

    def sentimentAnalysis(self, data, **kwargs):

        for entity, phrase in data.items():
            posCount = 0
            negCount = 0
            neuCount = 0
            positive = 0
            negative = 0

            result = {}
            '''Calculating percentage of ve+, ve-, and neutral phrases for each entity.
                Also calculating average percentage of ve+, ve- phrases for each entity'''
            for p in phrase:

                analysis = TextBlob(str(p))
                if analysis.sentiment.polarity > 0:
                    posCount += 1
                    positive += analysis.sentiment.polarity
                elif analysis.sentiment.polarity == 0:
                    neuCount += 1
                else:
                    negCount += 1
                    negative += analysis.sentiment.polarity

            percentPositive = float(posCount)/len(phrase) * 100
            percentNeutral = float(neuCount) / len(phrase) * 100
            percentNegative = float(negCount) / len(phrase) * 100
            result.update({entity:{'posC':percentPositive,
                                   'negC':percentNegative,
                                   'neuC':percentNeutral,
                                   'positive':positive/len(phrase),
                                   'negative':negative/len(phrase)}})
            # print(result)
            if kwargs['Source'] == 'Twitter':
                self.tweetSentiment.update(result)
            else:
                self.newsSentiment.update(result)

    def temporalAnalysis(self, dates, **kwargs):

        entityToDate = defaultdict(lambda : defaultdict(int))
        entitySum = defaultdict(int)
        result = {}
        if kwargs['Source'] == 'Twitter':
            for entity, date in dates.items():
                for d in date:
                    d = d.split(' ')
                    d = str(d[5])
                    entityToDate[entity][d] += 1
                    entitySum[entity] += 1

        if kwargs['Source'] == 'News':
            for entity, date in dates.items():
                for d in date:
                    d = d.date()
                    d = str(d.year)
                    entityToDate[entity][d] += 1
                    entitySum[entity] += 1

        for entity, dateCount in entityToDate.items():
            percentageList = [(float(count) / entitySum[entity]) * 100 for count in dateCount.values()]
            dateList = [year for year in dateCount.keys()]
            result.update({entity: [dateList, percentageList]})
        # print(result)

        if kwargs['Source'] == 'Twitter':
            self.tweetTemporal.update(result)
        else:
            self.newsTemporal.update(result)


    def spatialAnalysis(self, locations, **kwargs):

        entityToLocation = defaultdict(lambda : defaultdict(int))
        entitySum = defaultdict(int)
        for entity, loc in locations.items():
            for l in loc:
                entityToLocation[entity][l] += 1
                entitySum[entity] += 1
        result = {}
        code = {}
        for country in pycountry.countries:
            code[country.alpha_2] = country.name

        for entity, locCount in entityToLocation.items():
            percentageList = [(float(count)/entitySum[entity])*100 for count in locCount.values()]
            locationList = [code[loc] for loc in locCount.keys()]
            result.update({entity:[locationList, percentageList]})

        if kwargs['Source'] == 'Twitter':
            self.tweetSpatial.update(result)
        else:
            self.newsSpatial.update(result)

    def contentAnalysis(self, phrases, **kwargs):

        result = {}
        for entity, phrase in phrases.items():

            subjectivity = 0
            subCount = 0
            objectivity = 0
            objCount = 0

            for p in phrase:
                analysis = TextBlob(str(p))
                if analysis.sentiment.subjectivity >= 0.4:
                    subCount += 1
                    subjectivity += analysis.sentiment.subjectivity
                else:
                    objCount += 1
                    objectivity += (1 - analysis.sentiment.subjectivity)
            '''Calculating average subjectivity and objectivity for each entity.
                And percentage subjective and objective phrases for each entity'''

            result.update({entity:{'obj':float(objectivity)/len(phrase),
                                   'sub':float(subjectivity)/len(phrase),
                                   'objC':(float(objCount)/len(phrase))*100,
                                   'subC':(float(subCount)/len(phrase))*100}})
            # print(result)
            if kwargs['Source'] == 'Twitter':
                self.tweetContent.update(result)
            else:
                self.newsContent.update(result)
