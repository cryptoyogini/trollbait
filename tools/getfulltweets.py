#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 19:51:11 2018

@author: ananda
"""

import urllib2,pandas,sys
sys.path.append("/opt/hindi-tokenizer")
#from HindiTokenizer import Tokenizer
from bs4 import BeautifulSoup
textdf=pandas.read_csv("alltweetssomefulls.csv",encoding="utf-8")
for index,t in textdf.iterrows():
    if pandas.isnull(t['fulltext']):
        #tokenizer=Tokenizer(t['text'].encode("utf-8"))
        #tokenizer.tokenize()
        tb=t['text'].split(" ")
        for x in tb:
            if "http" in x:
                if "\n" in x:
                    x="https"+x.split("https")[1]
                print index,x
                try:
                    page=urllib2.urlopen(x).read()
                    print page
                    bs=BeautifulSoup(page)
                    mydivs = bs.findAll("div", {"class": "permalink"}) 
                    if len(mydivs)>0:
                        print unicode(mydivs[0])
                        textdf.at[index,'fulltext']=unicode(mydivs[0])
                except:
                    print "Oops!"