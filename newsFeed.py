# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com

import mongo
import aylien_news_api
from aylien_news_api.rest import ApiException

class NewsFeed():
    def __init__(self):

        aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'XXXXXX'

        aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'XXXXXXXXXXXXXXXXXX'

        self.api_instance = aylien_news_api.DefaultApi()

        self.opts = {
          'sort_by': 'relevance',
          'language': ['en'],
          'per_page': 100
        }

    def getNewsFeedAndStore(self, namedEntity, collection):
        print(namedEntity)
        title = {'title':namedEntity}
        self.opts.update(title)
        try:
            # List stories
            api_response = self.api_instance.list_stories(**self.opts)
            for story in api_response.stories:
                # print(story.title + " / " + story.source.name)
                description = " ".join(story.summary.sentences)
                try:
                    data = {'summary':description, 'source':story.source.locations[0].country,'published_at':story.published_at}
                except IndexError:
                    continue
                mongo.dataBase[collection].insert_one(data)
        except ApiException as e:
            print("Exception when calling DefaultApi->list_stories: %s\n" % e)