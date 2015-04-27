import twitter
import json
import CommonUtil
import numpy as np
from scipy.io import loadmat
CONSUMER_KEY = '2GvrOLlhgIXuo0oObvOXWqKsO'
CONSUMER_SECRET = 'BDnQLqmoQmSdImEF23mQdlt17touHHoCYz62SGZsUrs2T2L6Ax'
OAUTH_TOKEN = '1334170615-LqxQ7JdNohxttRL0RlSVhDSnPC08Sx5wOkgYW5T'
OAUTH_TOKEN_SECRET = 'kRr8b4DYVpikZVSsUYt7lD4FWFb3DnlbZwIud1Qy6w9lE'
num_of_features = 7
num_of_topics = 10
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

US_WOE_ID = 23424977

us_trends = twitter_api.trends.place(_id=US_WOE_ID)

# print the top 10 tweets
topics = []
for i in range(num_of_topics):
    name = us_trends[0]["trends"][i]["name"]
    print name
    topics.append(name)

outfile = open("test.txt", "w")
count = 10
for topic in topics:
    search_results = twitter_api.search.tweets(q=topic, count=count)
    statuses = search_results["statuses"]
    print len(statuses)
    row_num = 0
    while row_num < count:
        status = statuses[row_num]
        text = status["text"]
        # Message based features
        length_tweet = len(text)
        num_words = len(text.split())
        num_unique_chars = CommonUtil.count_unique_chars(text)
        num_hashtags = text.count("#")
        retweet_cnt = status["retweet_count"]
        num_swear_words = CommonUtil.count_swear_words(text)
        num_at_emotions = text.count("@")
        tweet_str = str(length_tweet) + "|" + str(num_words) + "|" + str(num_unique_chars) + "|" \
                    + str(num_hashtags) + "|" + str(retweet_cnt) + "|" + str(num_swear_words) + "|" \
                    + str(num_at_emotions)


        outfile.write(tweet_str)
        outfile.write("\n")
        row_num += 1
outfile.close()

#read file

f = open("test.txt", "r")
lineCnt = 0
for line in f:
    print line
    lineCnt+=1

print lineCnt

