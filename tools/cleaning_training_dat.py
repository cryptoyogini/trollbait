#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 01:36:41 2018

@author: lilhack110
"""
import re
from bs4 import BeautifulSoup
import pandas 
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()
 
tr_data= pandas.read_csv("/home/lilhack110/training.1600000.processed.noemoticon.csv")

tr_data.columns=['sentiment','id','date','query_string','user','text']
tr_data['sentiment'] = tr_data['sentiment'].map({0: 0, 4: 1})
tr_data.sort_values("date")
tr_data.drop(['id','date','query_string','user'],axis=1,inplace=True)  


pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))
def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        clean = stripped
    letters_only = re.sub("[^a-zA-Z]", " ", clean)
    lower_case = letters_only.lower()
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = tok.tokenize(lower_case)
    return (" ".join(words)).strip()
testing = tr_data.text[0:100]
result = []
for t in testing:
    result.append(tweet_cleaner(t)) 
nums = [0,400000,800000,1200000,1600000]
clean_df=pandas.DataFrame(result,columns=["text"])
clean_df.to_csv('train_clean_tweet.csv',encoding='utf-8')


print "Cleaning and parsing the tweets...\n"
clean_tweet_texts = []
for i in xrange(nums[0],nums[1]):
    if( (i+1)%10000 == 0 ):
        print "Tweets %d of %d has been processed" % ( i+1, nums[1] )                                                                    
    clean_tweet_texts.append(tweet_cleaner(tr_data['text'][i]))
    
print "Cleaning and parsing the tweets...\n"
for i in xrange(nums[1],nums[2]):
    if( (i+1)%10000 == 0 ):
        print "Tweets %d of %d has been processed" % ( i+1, nums[2] )                                                                    
    clean_tweet_texts.append(tweet_cleaner(tr_data['text'][i])) 
    
print "Cleaning and parsing the tweets...\n"
for i in xrange(nums[2],nums[3]):
    if( (i+1)%10000 == 0 ):
        print "Tweets %d of %d has been processed" % ( i+1, nums[3] )                                                                    
    clean_tweet_texts.append(tweet_cleaner(tr_data['text'][i]))


print "Cleaning and parsing the tweets...\n"
for i in xrange(nums[3],nums[4]):
    if( (i+1)%10000 == 0 ):
        print "Tweets %d of %d has been processed" % ( i+1, nums[4] )                                                                    
    clean_tweet_texts.append(tweet_cleaner(tr_data['text'][i]))
clean_df = pandas.DataFrame(clean_tweet_texts,columns=['text'])
clean_df['target'] = tr_data.sentiment
clean_df.head()

def make_fastText_input(df,fname):
    texts = df.text.values
    cat_id = df.target.values
    with open(fname, 'w') as f:
        for idx in range(df.__len__()):
            f.write('__label__' + str(cat_id[idx]) + ' ' + texts[idx].replace('\n', '') + '</s>\n')
    
  
clean_df = pandas.DataFrame(clean_tweet_texts,columns=['text'])
clean_df['target'] = tr_data.sentiment
make_fastText_input(clean_df,"cleaned_for_fasttext.txt")