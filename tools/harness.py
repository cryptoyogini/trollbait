#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 27 01:08:24 2018

@author: ananda
"""





import sys
sys.path.append("/opt/xetrapal/")
sys.path.append("../lib")
from HindiTokenizer import Tokenizer

import xetrapal
import analyze
x=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
t=x.get_twython()
gs=x.get_googledriver()
ws=gs.open_by_key("1xF7rqNVyr_VmoIojx3g__M57aV2cKPy6iWaD3YB6rnY")
df=ws.worksheet_by_title("datacleaning-orignotnull").get_as_df()
df['cleantext']=df.fulltextsqueezed.apply(analyze.clean)



