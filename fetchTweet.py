import twitter
import json
import CommonUtil
from Tweet import Tweet
from django.utils.encoding import smart_str, smart_unicode
import numpy as np
from scipy.io import loadmat



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

outfile1 = open("full_info.txt", "w")
outfile2 = open("matrix_info.txt", "w")
total_count = 100
count_per_search = 100
topic_counter = 0
num_positive = 0
num_negative = 0
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
            annotation = t.annotate()
            tweet_str1 =  smart_str(text) + str(t.length_tweet) + "|" + "Num words:"+ str(t.num_words) + "|" + "Num unique chars:"+ str(t.num_unique_chars) + "|" \
                        + "Num #:"+str(t.num_hashtags) + "|" + "Retweets:"+ str(t.retweet_cnt) + "|" + "Swear words:"+ str(t.num_swear_words) + "|" \
                        + "Num @:"+str(t.num_at_emotions) + "|" \
                        + "Registration age:"+str(t.registration_age) + "|" + "Followers:"+str(t.num_followers) + "|" + "Followee:"+str(t.num_followee) + "|" \
                        + "Is verified:"+str(t.is_verified) + "|" + "Len desc:"+str(t.len_desc) + "|" + "Len Screen name:"+str(t.len_screen_name) + "|" \
                        + "Has url:"+str(t.has_url) + "|" \
                        + "Annotation:"+str(annotation) + "|"
            tweet_str2 =  str(t.length_tweet) + "|" + str(t.num_words) + "|" + str(t.num_unique_chars) + "|" \
                        + str(t.num_hashtags) + "|" + str(t.retweet_cnt) + "|" +  str(t.num_swear_words) + "|" \
                        + str(t.num_at_emotions) + "|" \
                        + str(t.registration_age) + "|" + str(t.num_followers) + "|" + str(t.num_followee) + "|" \
                        + str(t.is_verified) + "|" + str(t.len_desc) + "|" + str(t.len_screen_name) + "|" \
                        + str(t.has_url) + "|" \
                        + str(annotation)

            if annotation == 1:
                num_positive += 1
            else:
                num_negative +=1
            outfile1.write(tweet_str1)
            outfile1.write("\n")
            outfile2.write(tweet_str2)
            outfile2.write("\n")
            row_num += 1
        count_fetched += search_results_len
    print "-------------------------------------------------"
outfile1.close()
outfile2.close()
print "Num of positive tweets ", num_positive
print "Num of negative tweets ", num_negative
#read file

f = open("matrix_info.txt", "r")
lineCnt = 0
for line in f:
    #print line
    lineCnt+=1

print lineCnt

