# twitter-analysis - 12/03/2018
--------------------------------

This project does a sentiment, temporal, spatial and content analysis of random tweets and news feeds.
The analysis is done only for named-entities.
Corresponding graphs are then plotted comparing the tweets and news results.

# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com

Description:

The twitter search api is used to collect 10,0000 tweets. The tweets are then tokenized 
using regular expression operations, nltk corpus is used to filter out stopwords, any leading 
characters like '@', '#', '&' or 'https' are removed. After this the remaining words are
tagged as 'Part of Speech' using nltk. Since we only want named entities, only the words 
tagged as 'NNP' i.e. pronouns are used. Also, any seperated named entity is concatenated.
These words are finally given to the Stanford Named Entity Tagger. The words are tagged 
in four categories namely LOCATION, PERSON, ORGANIZATION or OTHERS. A final filter is run to 
remove all entities tagged as OTHERS. The top five most frequent words appearing in the remaining 
lot are selected. Based on these named entities news articles are searched using the aylien news-api.
Once the news articles are collected, they are sent for the same preprocessing as the tweets 
were. Then the analysis is done.

All the analysis is done for the tweets and news articles containing the common-named entities.

Sentiment Analysis: 
This is done using Text Blob with its default 'Pattern Analyzer' model.
A positive sentence has a score greater than zero but less than 1. A negative sentence has a 
score between -1 and 0, a score of zero denotes a neutral sentence. The percentage tweets and 
news articles are categorized as being positive, negative, neutral and plotted.

Temporal Analysis: 
This is the analysis pertaining to the date and time of the tweets or news articles. A 
distribution of the percentage tweets and news articles across different years is plotted.


Spatial Analysis:
This deals with the distribution of the tweets and news articles across different geographical
locations. We get an idea of the popularity of the named entities in different regions of the world.

Content Analysis:
This is done to get a social understanding of the content. Here TextBlob is used to get the subjectivity 
and objectivity of the tweets and news articles. The score given to a sentence varies between 0 to 1, i.e
objective to subjective.
