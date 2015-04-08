import twitter
import json
import CommonUtil
CONSUMER_KEY = 
CONSUMER_SECRET = 
OAUTH_TOKEN = 
OAUTH_TOKEN_SECRET = 

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

US_WOE_ID = 23424977

us_trends = twitter_api.trends.place(_id=US_WOE_ID)
print json.dumps(us_trends, indent=1)

# print the top 3 tweets
topTweets = []
for i in range(3):
    name = us_trends[0]["trends"][i]["name"]
    print name
    topTweets.append(name)

q = topTweets[0]
count = 1
search_results = twitter_api.search.tweets(q=q, count=count)

# print json.dumps(search_results, indent=1)

statuses = search_results["statuses"]
status = statuses[0]
text = status["text"]

# Message based features
print "Text:", text
print "Length of the tweet:", len(text)
print "NUmber of words:", len(text.split())
print "Number of unique chars:", CommonUtil.count_unique_chars(text)
print "Number of hashtags:", text.count("#")
print "Retweet count:", status["retweet_count"]
print "Number of swear words:", CommonUtil.count_swear_words(text)
print "Number of @ emotions:", text.count("@")


# Source based features


