import twitter
import json
import CommonUtil
import numpy as np
from scipy.io import loadmat
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import RunSVM




num_of_features = 7
num_of_topics = 10
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

US_WOE_ID = 23424977
WORLD_WOE_ID = 1

highEvents = []
highEvents.append('#BlackLivesMatter')
highEvents.append('#nepalearthquake')
highEvents.append('#baltimoreriots')

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        global x
        x = self
        print("Client connecting: {0}".format(request.peer))	

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        print("Client Called me..."+payload)
        count_per_search = 100

        if payload == "Show Trends":
            us_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
            print us_trends
            topics = []
            for i in range(num_of_topics):
                name = us_trends[0]["trends"][i]["name"]
                print name
                topics.append(name)
            print(topics)
            self.sendMessage(str(1))
            self.sendMessage(str(topics).strip('[]'))

        elif payload == "Filtering":
            for event in highEvents:
                search_results = twitter_api.search.tweets(q=event, count=count_per_search)
                tweets = search_results["statuses"]
        else:
            topic_name = payload
            tweet_text_str=RunSVM.fetch_tweets_for_topic(topic_name)
            print(tweet_text_str)
            self.sendMessage(str(0))
            self.sendMessage(str(tweet_text_str))


        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8'))) 

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))         

    def onDisconnect(self):
        reactor.stop()

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()

