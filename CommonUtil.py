import pickle
import time
import re
from datetime import datetime
# http://en.wiktionary.org/wiki/Category:English_swear_words
swear_words = {"arse", "ass", "asshole", "bastard", "bitch", "bloody", "bollocks", "child-fucker",
               "Christ on a bike", "Christ on a cracker", "cunt", "damn", "fuck", "goddamn", "godsdamn"
               "hell", "holy shit", "Jesus", "Jesus Christ", "Jesus H. Christ", "Jesus Harold Christ",
               "Jesus wept", "Jesus, Mary and Joseph", "Judas Priest", "motherfucker",  "shit"
               "shit ass", "shitass", "son of a bitch", "son of a motherless goat", "son of a whore",
               "sweet Jesus"}
fp = open("posW","r+")
fn = open("posN","r+")
positiveWords = pickle.load(fp)
negativeWords = pickle.load(fn)

smiley_pattern = '^(:-\(|:-\))+$' # matches only the smileys ":-)" and ":-("
smiley_matcher = re.compile(smiley_pattern)


def count_unique_chars(inp):
    d = {}
    for letter in inp:
        if letter in d:
            count = d[letter]+1
            d[letter] = count+1
        else:
            d[letter] = 1
    return d.keys().__len__()


def count_swear_words(inp):
    count = 0
    for swear_word in swear_words:
        if swear_word.lower() in inp.lower():
            count += 1
    return count
print count_swear_words("Test")


def file_len(fname):
    cnt = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            cnt += 1
    return cnt


def count_pos_words(inp):
    count = 0
    words = inp.split()
    for word in words:
        if word in positiveWords:
            count += 1
    return count


def count_neg_words(inp):
    count = 0
    words = inp.split()
    for word in words:
        if word in negativeWords:
            count += 1
    return count


def count_num_days_from_today(inp):
    d1 = datetime.strptime(inp, '%a %b %d %H:%M:%S +0000 %Y')
    today = time.strftime('%Y-%m-%d')
    d2 = datetime.strptime(today, '%Y-%m-%d')
    return (d2-d1).days


def count_num_emoticons(inp):
    count = 0
    words = inp.split()
    for word in words:
        if smiley_matcher.match(word):
            count += 1
    return count