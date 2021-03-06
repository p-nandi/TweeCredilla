import twitter
import json
import CommonUtil
import numpy as np
from scipy.io import loadmat

CONSUMER_KEY = 'vd25o5blsk9T9IBjZUXgtdlTF'
CONSUMER_SECRET = '8qY6uDU8hBJz9JCoamGVLJe01Upo3fKm2NN4jr1NVvBBa84dmu'
OAUTH_TOKEN = '70677289-pV7SOWATIvoPlyNraeqJXDHNkXdNnvbXa720sKQYM'
OAUTH_TOKEN_SECRET = '5cbHS2sfEC0UGVIuapTValUzQXwvfi4WAVKNjhVhmRMD2'

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
total_count = 1
count_per_search = 1
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
            status = statuses[row_num]
            print status
            resp = json.dumps(status, indent=4)
            print resp
            text = status["text"]
            # Message based features
            length_tweet = len(text)
            num_words = len(text.split())
            num_unique_chars = CommonUtil.count_unique_chars(text)
            num_hashtags = text.count("#")
            retweet_cnt = status["retweet_count"]
            max_id = status["id"]
            num_swear_words = CommonUtil.count_swear_words(text)
            num_at_emotions = text.count("@")

            # Source based Features
            user_features = status["user"]
            num_followers = user_features["followers_count"]
            num_friends = user_features["friends_count"]
            is_verified = user_features["verified"]
            if is_verified:
                is_verified = 1
            else:
                is_verified = 0
            len_desc = len(user_features["description"])
            len_screen_name = len(user_features["screen_name"])
            user_url = user_features["url"]
            print "user_url", user_url
            has_url = 0
            if user_url:
                has_url = 1
            user_creation_date = user_features["created_at"]
            print user_creation_date
            # Create tweet characteristics to write to file
            tweet_str = str(length_tweet) + "|" + str(num_words) + "|" + str(num_unique_chars) + "|" \
                        + str(num_hashtags) + "|" + str(retweet_cnt) + "|" + str(num_swear_words) + "|" \
                        + str(num_at_emotions)


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

