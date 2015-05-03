__author__ = 'phantom'
import numpy as np
from sklearn import svm
from Tweet import Tweet
import twitter
from twitter import oauth
#from twitter import Twitter
import json
import CommonUtil
from django.utils.encoding import smart_str, smart_unicode



def preprocess():
    n_features = 14
    n_sample = 5000
    train_data = np.zeros((n_sample, n_features+1), dtype=np.int)
    f = open("matrix_info.txt", "r")
    row_index = 0
    for line in f:
        row_data=line.split("|")
        column_index = 0
        for data in row_data:
            train_data[row_index][column_index] = data
            column_index += 1
        row_index += 1
    f.close()
    train_label = train_data[:, n_features:]
    train_data = train_data[:, 0:n_features]
    return train_data, train_label


def run_svm(train_data, train_label):
    train_label = train_label.ravel()
    # Radial basis function , gamma = 1.0
    print('\n--------Radial basis function , Gamma Default-------------------')
    clf = svm.SVC(kernel='rbf', gamma=0.0);
    clf.fit(train_data, train_label);
    predicted_label = clf.predict(train_data)
    print('\n Radial basis function Gamma default Train set Accuracy:' + str(100*np.mean((predicted_label == train_label).astype(float))) + '%')
    return clf


def fetch_new_tweets():
    num_of_topics = 1
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)


    US_WOE_ID = 23424977
    WORLD_WOE_ID = 1

    tweet_list = []

    us_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)

    # print the top 10 tweets
    topics = []
    for i in range(num_of_topics):
        name = us_trends[0]["trends"][i]["name"]
        print name
        topics.append(name)
    total_count = 500
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
                #print status
                resp = json.dumps(status, indent=4)
                #print resp
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
                tweet_str =  smart_str(text) + "|" + str(t.length_tweet) + "|" + str(t.num_words) + "|" + str(t.num_unique_chars) + "|" \
                            + str(t.num_hashtags) + "|" + str(t.retweet_cnt) + "|" +  str(t.num_swear_words) + "|" \
                            + str(t.num_at_emotions) + "|" \
                            + str(t.registration_age) + "|" + str(t.num_followers) + "|" + str(t.num_followee) + "|" \
                            + str(t.is_verified) + "|" + str(t.len_desc) + "|" + str(t.len_screen_name) + "|" \
                            + str(t.has_url)
                tweet_list.append(tweet_str)

                row_num += 1
            count_fetched += search_results_len
    return tweet_list


def predict_label(clf, tweet_list):
    n_features = 14
    row_index = 0
    n_sample = len(tweet_list)
    test_data = np.zeros((n_sample, n_features+1), dtype=np.int)
    tweet_text_list = []
    outfile = open("tweet_prediction.txt", "w")
    for tweet in tweet_list:
        row_data = tweet.split("|")
        tweet_text = row_data[0]
        tweet_text_list.append(tweet_text)
        row_data = row_data[1:]
        column_index = 0
        for data in row_data:
            test_data[row_index][column_index] = data
            column_index += 1
        row_index += 1
    print "Actual Tweet Size", len(tweet_text_list)
    predicted_label = clf.predict(test_data)
    pl_index = 0
    for tweet_text in tweet_text_list:
        tweet_text = tweet_text + "|" + predict_label[pl_index]
        pl_index += 1
        outfile.write(tweet_text)
    outfile.close()


train_data, train_label = preprocess()
clf = run_svm(train_data, train_label)
tweet_list = fetch_new_tweets()
predict_label(clf,tweet_list)
