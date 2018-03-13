# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com

import tweetCollection
import newsFeed
import analysis

'''Enter collection names to store news and tweet data'''
newsCollectionName = None
# newsCollectionName = 'newsData'
tweetCollectionName = None
#tweetCollectionName = 'randomTweetData'

if __name__ == '__main__':

    '''Create data collection object and call method to fetch and store tweets in database.'''
    tweetHandle = tweetCollection.TwitterDataCollection()
    tweetHandle.fetchTweetsAndStore(tweetCollectionName)

    '''Create data processing object'''
    processData = tweetCollection.ProcessDataForNamedEntities()

    '''fetchData sets cursor to appropriate collection in database.'''
    processData.fetchData(tweetCollectionName)
    '''Get frequent words and list of phrases after filtering tweets'''
    frequentWords, tweetsEntityList = processData.getNamedEntities(FrequentTerms=True)


    '''Collect news feeds based on frequent words'''
    newsHandle = newsFeed.NewsFeed()
    for name in frequentWords:
        newsHandle.getNewsFeedAndStore(name[0], newsCollectionName)

    '''fetchData sets cursor to appropriate collection in database.'''
    processData.fetchData(newsCollectionName)
    '''get filtered data'''
    newsEntityList = processData.getNamedEntities(FrequentTerms=False)

    '''Gather data for analysis and plot graphs.'''
    analysis = analysis.Analysis(frequentWords)
    processData.fetchData(tweetCollectionName)
    dates, locations, phrases = processData.fetchDataForAnalysis(frequentWords, tweetsEntityList, Source='Twitter')


    analysis.temporalAnalysis(dates, Source = 'Twitter')
    analysis.contentAnalysis(phrases, Source = 'Twitter')
    analysis.spatialAnalysis(locations, Source = 'Twitter')
    analysis.sentimentAnalysis(phrases, Source = 'Twitter')

    processData.fetchData(newsCollectionName)
    dates, locations, phrases = processData.fetchDataForAnalysis(frequentWords, newsEntityList, Source='News')


    analysis.temporalAnalysis(dates, Source = 'News')
    analysis.contentAnalysis(phrases, Source = 'News')
    analysis.spatialAnalysis(locations, Source = 'News')
    analysis.sentimentAnalysis(phrases, Source = 'News')

    analysis.plotGraph()