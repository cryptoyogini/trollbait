#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:51:11 2018

@author: ananda
"""
import urllib2,pandas,sys
sys.path.append("/opt/hindi-tokenizer")
from bs4 import BeautifulSoup

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
                    






textdf=pandas.read_csv("alltweetssomefulls.csv",encoding="utf-8")
 