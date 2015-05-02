class Tweet:
    text = ""
    length_tweet = 0
    num_words = 0
    num_unique_chars = 0
    num_hashtags = 0
    retweet_cnt = 0
    num_swear_words = 0
    num_at_emotions = 0
    registration_age = 0
    num_followers = 0
    num_followee = 0
    ratio_foll_followee = 0
    is_verified = 0
    len_desc = 0
    len_screen_name = 0
    has_url = 0
    is_positive = 0

    def __init__(self):
        self.is_positive = 0

    def annotate(self):
        if self.is_verified == 1 or self.num_followers > 2000 or self.retweet_cnt > 10:
            self.is_positive = 1
        else:
            self.is_positive = 0
        return self.is_positive
