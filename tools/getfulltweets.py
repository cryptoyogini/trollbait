#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:51:11 2018

@author: ananda
"""

import urllib2,pandas
from bs4 import BeautifulSoup
textdf=pandas.read_csv("alltweets.csv",encoding="utf-8")
for index,t in textdf.iterrows():
    tb=unicode(t.text).split(" ")
    for x in tb:
        if "http" in x:
            page=urllib2.urlopen(x).read()
            bs=BeautifulSoup(page)
            mydivs = bs.findAll("div", {"class": "tweet-text"}) 
            if len(mydivs)>0:
                print unicode(mydivs[0])
                textdf.at[index,'fulltext']=unicode(mydivs[0])
