#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:51:11 2018

@author: ananda
"""
import urllib2,pandas,sys
sys.path.append("/opt/hindi-tokenizer")
from bs4 import BeautifulSoup
import re
import langdetect
retweetcountre=r'([0-9,]+\sretweet[s]*)'
retweetcount=re.compile(retweetcountre)

likecountre=r'([0-9,]+\slike[s]*)'
likecount=re.compile(likecountre)


replycountre=r'([0-9,]+\sreply|[0-9,]+\sreplies)'
replycount=re.compile(replycountre)     


twitterhandlere=r'(@\w{1,15})\b'
twitterhandle=re.compile(twitterhandlere)
def get_num_retweets(text):
   if type(text)!=str and type(text)!=unicode:
       return 0
   a=re.findall(retweetcount,text)
   #print a[0]
   if len(a)>0:
      return int(a[0].split(" ")[0].replace(",",""))
   else:
       return 0

def get_num_replies(text):
   if type(text)!=str and type(text)!=unicode:
       return 0
   a=re.findall(replycount,text)
   #print a[0]
   if len(a)>0:
      return int(a[0].split(" ")[0].replace(",",""))
   else:
       return 0
   
def has_hindi(text, numpasses=2):
    if type(text)!=str and type(text)!=unicode:
       return False
    possibles=[]
    for i in range(int(numpasses)):
        possibles=possibles+langdetect.detect_langs(text)
    possibles=list(set(possibles))
    print possibles
    for lang in possibles:
        if lang.lang in [u'ne',u'hi',u'mr']:
            return True
    return False

def get_all_handles(text):
    return list(set(re.findall(twitterhandle,text)))
    
def get_full_tweets(textdf,startindex=0):
    for index,t in textdf.iterrows():
        if index>=startindex:
            tb=t['text'].split(" ")
            for x in tb:
                if "http" in x:
                    if "\n" in x:
                        x="https"+x.split("https")[1]
                    print index,x
                    #try:
                    try:
                        page=urllib2.urlopen(x).read()
                    #print page
                    except:
                        page=""
                    bs=BeautifulSoup(page)
                    mydivs = bs.findAll("div", {"class": "permalink-in-reply-tos"}) + bs.find_all("div",{"class":"permalink-tweet"})
                    fulltext=""
                    if len(mydivs)>0:
                        for div in mydivs:
                            fulltext=fulltext+div.get_text()
                    fulltext=fulltext.replace("  "," ").replace("\n"," ").replace("Verified account"," ").replace("Unblock", "").replace("Unfollow", "").replace("Blocked", "").replace("Pending", "").replace("Show this thread", "").replace("Following","").replace("Follow","")
                    print fulltext
                    textdf.at[index,'fulltext']=fulltext.encode("utf-8")
                    textdf.to_csv("alltweetssomefulls.csv",encoding="utf-8",index=False)
                    print "Completed processing record " + str(index)
                    



def clean_junk(text):
    text=text.lstrip(" ").rstrip(" ")
    text=re.sub("\s+"," ",text)
    pass1=re.sub(likecount," ",text)
    #print "Removed likecount " , pass1
    pass2=re.sub(replycount," ",pass1)
    #print "Removed replycount " , pass2
    
    pass3=re.sub(retweetcount," ",pass2)
    #print "Removed retweetcount " , pass3
    
    pass4=re.sub("\s\s+","%%",pass3)
    #print "After splitting ", pass4
    return pass4.split("%%")[0]


#textdf=pandas.read_csv("alltweetssomefulls.csv",encoding="utf-8")
 