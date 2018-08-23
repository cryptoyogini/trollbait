#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 19:04:55 2018

@author: lilhack110
"""
import sys
sys.path.append("/opt/xetrapal")
import xetrapal
import tweepy
import pandas
import datetime
import math
import json
from sklearn.feature_extraction.text import CountVectorizer 



ananda=xetrapal.Xetrapal(configfile="/home/lilhack110/ab.conf")
anandatw=ananda.get_twython()
anandagd=ananda.get_googledriver()
twconfig=xetrapal.karma.get_section(ananda.config,"Twython")
tweep=get_tweepy(twconfig)
trollbaitsheet=anandagd.open_by_key(key="1zisiKnhF4cEW4H7fvhpZ7Y8cGfwQybvGgDg6Jnth5j4")
