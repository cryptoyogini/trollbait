#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:32:54 2018

@author: lilhack110
"""
names_journalists=['sudhirchaudhary',
'sardanarohit',
'KishoreAjwani',
'ravishndtv',
'dcindianews',
'VinodDua7',
'RajatSharmaLive',
'awasthis',
'abhisar_sharma',
'dibang',
'nehapant1',
'romanaisarkhan',
'anjanaomkashyap',
'SwetaSinghAT',
'RubikaLiyaquat',
'NidhiKNDTV',
'NaghmaNDTV',
'SharmaKadambini',
'poornima_mishra',
'avasthiaditi']
import json
from twython import Twython
from twython import TwythonStreamer
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

search = t.search(q='RajatSharmaLive', 
                    
                  
                    )

tweets = search['statuses']
count=000
for tweet in tweets:
    count+=1
    print tweet['id_str'], '\n', tweet['text'], '\n\n\n'
#with open('tweets.txt', 'w') as f:geocode='-74,40,-73,41',
                    
  #json.dump(data, f, ensure_ascii=False)

class MyStreamer(TwythonStreamer):
  tweets=[] 
  def on_success(self, data):
    if 'text' in data:
        tweet= data['text'].encode('utf-8')
        if 'Accounting' in tweet:
          tweets.append(tweet)
          print tweet

  def on_error(self, status_code, data):
    print status_code
    self.disconnect()

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


stream.statuses.filter()