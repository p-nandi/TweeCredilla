__author__ = 'bikramka'
import os
import pickle
positiveWords=set()
negativeWords=set()
fp = open("posW","w+")
fn = open("posN","w+")
fo=open("/home/bikramka/Studies/706/AFINN/AFINN-111.txt","r+")
fo=open("AFINN-111.txt","r+")
for line in fo:
    tokens = line.split("\t")
    value = int(tokens[1])
    if value>0:
        positiveWords.add(tokens[0])
    if value<0:
        negativeWords.add(tokens[0])

print len(positiveWords)
print len(negativeWords)
pickle.dump(positiveWords,fp)
pickle.dump(negativeWords,fn)

