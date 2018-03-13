# Author: Harsh Vardhan Singh
# hvsingh.in@gmail.com

import plotly
import plotly.graph_objs as go

entityName = 'Modi'
def sentimentGraph(tweet, news, entityName):
    trace1 = go.Bar(
        x=['Positive(%)', 'Neutral(%)', 'Negative(%)'],
        y=[tweet['posC'], tweet['neuC'], tweet['negC']],
        name='Tweets',
        text=['Average positivity' + str(tweet['positive']), ' ', 'Average negativity' + str(tweet['negative'])]
    )
    trace2 = go.Bar(
        x=['Positive(%)', 'Neutral(%)', 'Negative(%)'],
        y=[news['posC'], news['neuC'], news['negC']],
        name='News',
    text=['Average positivity ' + str(news['positive']), ' ', 'Average negativity ' + str(news['negative'])]
    )

    data = [trace1, trace2]
    layout = go.Layout(
        title='Sentiment Analysis for ' + entityName +'. This graph gives the percentage tweets and news items that were either positive, neutral or negative.',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,  filename='grouped-text-hover-bar.html')

def contentGraph(tweets, news, entityName):
    trace1 = go.Bar(
        x=['Subjective(%)', 'Objective(%)'],
        y=[tweets['subC'], tweets['objC']],
        name='Tweets',
        text=['Average Subjectivity ' + str(tweets['sub']),  'Average Objectivity ' + str(tweets['sub'])]
    )
    trace2 = go.Bar(
        x=['Subjective(%)', 'Objective(%)'],
        y=[news['subC'], news['objC']],
        name='News',
        text=['Average Subjectivity ' + str(news['sub']),  'Average Objectivity ' + str(news['sub'])]
    )

    data = [trace1, trace2]
    layout = go.Layout(
        title='Content Analysis for ' + entityName +'. This graph gives the percentage tweets and news items that were either subjective or objective in nature.',
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,  filename='grouped-text-hover-bar.html')

def spatialGraph(tweets, news, entityName):
    fig = {
      "data": [
        {
          "values": tweets[1],
          "labels": tweets[0],
          "domain": {"x": [0, .47]},
          "hoverinfo":"label+percent",
          "hole": .4,
          "type": "pie"
        },
        {
          "values": news[1],
          "labels": news[0],
          "domain": {"x": [.53, 1]},
          "hoverinfo":"label+percent",
          "hole": .4,
          "type": "pie"
        }],
      "layout": {
            "title":"Spatial Analysis of " + entityName,
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Tweets",
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "News",
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    }
    plotly.offline.plot(fig, filename='donut.html')

def temporalGraphs(tweets, news, entityName):
    trace1 = go.Bar(
        x=tweets[0],
        y=tweets[1],
        name='Tweets',
    )
    trace2 = go.Bar(
        x=news[0],
        y=news[1],
        name='News',
    )
    layout = go.Layout(
        title='Temporal Analysis for ' + entityName + '. This graph gives the percentage tweets and news items per year.',
    )
    data = [trace1, trace2]

    fig = dict(data=data, layout = layout)
    plotly.offline.plot(fig, filename='grouped-text-hover-bar.html')