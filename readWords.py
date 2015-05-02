__author__ = 'bikramka'
import pickle
fp = open("posW","r+")
fn = open("posN","r+")
positiveWords = pickle.load(fp)
negativeWords = pickle.load(fn)
print positiveWords
print negativeWords
