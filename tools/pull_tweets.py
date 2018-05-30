#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:32:54 2018

@author: lilhack110
"""
#removed neha pant from the list as it was not producing any output
names_journalists=[
'romanaisarkhan',
'anjanaomkashyap',
'SwetaSinghAT',
'RubikaLiyaquat',
'SharmaKadambini',
'poornima_mishra',
'avasthiaditi','sudhirchaudhary',
'sardanarohit',
'KishoreAjwani',
'ravishndtv',
'dcindianews',
'VinodDua7',
'RajatSharmaLive',
'awasthis',
'abhisar_sharma',
'dibang']
names_femalejounalists=[]
import json,time,pandas
from twython import Twython
#from twython import TwythonStreamer
TWITTER_APP_KEY = 'Cc9kj80mLNobWn2swX12HHt2L'
TWITTER_APP_KEY_SECRET = 'nPPwwP9ZZHwdMs1r7vzwemMvuLI7pjBsyly951EfjzTrO2MGpK'
TWITTER_ACCESS_TOKEN = '90339443-NXHrWJ6i3IJGJ7hmNWWUUjzrkBhPsW4lEH36AGtko'
TWITTER_ACCESS_TOKEN_SECRET = 'WPVF3qFDU5f3qGf237lsnsmiUWW4Mydir14jZKC6GWTK3'
APP_KEY = 'Cc9kj80mLNobWn2swX12HHt2L'
APP_SECRET = 'nPPwwP9ZZHwdMs1r7vzwemMvuLI7pjBsyly951EfjzTrO2MGpK' 
OAUTH_TOKEN = '90339443-NXHrWJ6i3IJGJ7hmNWWUUjzrkBhPsW4lEH36AGtko'
OAUTH_TOKEN_SECRET = 'WPVF3qFDU5f3qGf237lsnsmiUWW4Mydir14jZKC6GWTK3'
t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)


def get_tweets_for_handle(handle, tcount, maxtries=10):
    tweets=[]
    p=t.search(q=handle,count=tcount)['statuses']
    tries=0
    while len(tweets)<tcount:
        
        tweets=tweets+p
        p=t.search(q='@'+handle,count=100,max_id=p[-1]['id'])['statuses']
        print "Sleeping..."
        time.sleep(5)
        print len(tweets)
        tries+=1
        if(tries>maxtries):
            break
        
    return tweets[:tcount]
alltweets=[]
for name in names_journalists:

    

    all_tweets=get_tweets_for_handle(name,500)
    alltweets.append(all_tweets)
alltweets= pandas.DataFrame(alltweets)
for tweets in alltweets.columns:
    with open(str(names_journalists)+'.txt', 'w') as tweet:
        json.dump(alltweets,tweet)
        
    
     



    


    
    
    