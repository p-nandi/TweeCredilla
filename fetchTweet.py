import twitter
import json
import CommonUtil
from Tweet import Tweet
import numpy as np
from scipy.io import loadmat
CONSUMER_KEY = '2GvrOLlhgIXuo0oObvOXWqKsO'
CONSUMER_SECRET = 'BDnQLqmoQmSdImEF23mQdlt17touHHoCYz62SGZsUrs2T2L6Ax'
OAUTH_TOKEN = '1334170615-LqxQ7JdNohxttRL0RlSVhDSnPC08Sx5wOkgYW5T'
OAUTH_TOKEN_SECRET = 'kRr8b4DYVpikZVSsUYt7lD4FWFb3DnlbZwIud1Qy6w9lE'

num_of_features = 7
num_of_topics = 1
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

US_WOE_ID = 23424977
WORLD_WOE_ID = 1

us_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)

# print the top 10 tweets
topics = []
for i in range(num_of_topics):
    name = us_trends[0]["trends"][i]["name"]
    print name
    topics.append(name)

outfile = open("test.txt", "w")
total_count = 100
count_per_search = 100
topic_counter = 0
for topic in topics:
    topic_counter += 1
    print "topic #", topic_counter
    count_fetched = 0
    max_id = -1
    while count_fetched < total_count:
        row_num = 0
        search_results = twitter_api.search.tweets(q=topic, count=count_per_search, max_id=max_id)
        statuses = search_results["statuses"]
        search_results_len = len(statuses)
        # per tweet processing
        while row_num < count_per_search:
            t = Tweet()
            status = statuses[row_num]
            print status
            resp = json.dumps(status, indent=4)
            print resp
            text = status["text"]
            t.text = text
            # Message based features
            t.length_tweet = len(text)
            t.num_words = len(text.split())
            t.num_unique_chars = CommonUtil.count_unique_chars(text)
            t.num_hashtags = text.count("#")
            t.retweet_cnt = status["retweet_count"]
            max_id = status["id"]
            t.num_swear_words = CommonUtil.count_swear_words(text)
            t.num_at_emotions = text.count("@")

            # Source based Features
            user_features = status["user"]
            t.registration_age = CommonUtil.count_num_days_from_today(user_features["created_at"])
            t.num_followers = user_features["followers_count"]
            t.num_followee = user_features["friends_count"]
            if t.num_followee !=0:
                   t.ratio_foll_followee = t.num_followers / t.num_followee
            is_verified = user_features["verified"]
            if is_verified:
                t.is_verified = 1
            else:
                t.is_verified = 0
            t.len_desc = len(user_features["description"])
            t.len_screen_name = len(user_features["screen_name"])
            user_url = user_features["url"]
            if user_url:
                t.has_url = 1
            # Create tweet characteristics to write to file
            tweet_str =  str(t.length_tweet) + "|" + str(t.num_words) + "|" + str(t.num_unique_chars) + "|" \
                        + str(t.num_hashtags) + "|" + "Retweets:"+str(t.retweet_cnt) + "|" + str(t.num_swear_words) + "|" \
                        + str(t.num_at_emotions) + "|" \
                        + "Registration age:"+str(t.registration_age) + "|" + "Followers:"+str(t.num_followers) + "|" + "Followee:"+str(t.num_followee) + "|" \
                        + "Is verified:"+str(t.is_verified) + "|" + "Len desc:"+str(t.len_desc) + "|" + "Len Screen name:"+str(t.len_screen_name) + "|" \
                        + "Has url:"+str(t.has_url) + "|" \
                        + "Annotation:"+str(t.annotate()) + "|"
            print tweet_str
            outfile.write(tweet_str)
            outfile.write("\n")
            row_num += 1
        count_fetched += search_results_len
        print "count_fetched", count_fetched
    print "-------------------------------------------------"
outfile.close()

#read file

f = open("test.txt", "r")
lineCnt = 0
for line in f:
    #print line
    lineCnt+=1

print lineCnt

