#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 14:07:56 2018

@author: lilhack110
"""
import re
from bs4 import BeautifulSoup
import pandas 
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()

def txt_to_csv(filename):
    with open(filename,'r') as f:
        dat=f.read()
        datlist=dat.strip().split("ENDOFTWEET")
        mendatseries=pandas.Series(datlist)
        mendatdf=pandas.DataFrame(datlist)

        
        mendatdf.columns= ["tweets"]
            
        return mendatdf
    
a=txt_to_csv("/home/lilhack110/fastText-0.1.0/trollbait/mentweets1000.txt")    
    
 
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))


def asli_tweet_cleaner(text):
    twitterhandlere=r'(@\w{1,15})\b'
    twitterhandle=re.compile(twitterhandlere)
    linkre= r'https?://[A-Za-z0-9./]+'
    link=re.compile(linkre)
    outtext=text.replace(twitterhandle,"",text)
    outtext=outtext.replace(link,"",text)
    return outtext

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
testing = a.tweets 
result = []
for t in testing:
    result.append(tweet_cleaner(t))
result    
clean_df = pandas.DataFrame(result,columns=['text']) 
clean_df=clean_df.dropna(subset=["text"])  
def make_fastText_input(df,fname):
    texts = df.text.values
#    cat_id = df.target.values
    with open(fname, 'w') as f:
        for idx in range(df.__len__()):
            f.write(texts[idx].replace('\n', '') + '</s>\n')      
