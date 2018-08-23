import sys,os
sys.path.append("/opt/xetrapal")
sys.path.append("../lib")
import xetrapal
import tweepy
import pandas
import datetime
import math
import json
from sklearn.feature_extraction.text import CountVectorizer 
from tqdm import tqdm
import collections

sys.path.append("/opt/livingdata/lib")
from HindiTokenizer import Tokenizer



def wordcount(text,logger=xetrapal.astra.baselogger):
    wordFreq = collections.Counter()
    t=Tokenizer(text)
    logger.info("Beginning generate word count on input")
    logger.info("Tokenizing the input")
    t.tokenize()
    parsedText = t.tokens
    
    # clean up and count word
    while "" in parsedText:
        parsedText.remove("")
    for word in tqdm(parsedText):
		if word == '':
			continue
		# add word to count
		wordFreq[word] += 1     
    return wordFreq

def load_tweets_from_json(filename):
    print filename
    with open(filename,"r") as f:
        tweetdf=pandas.DataFrame(json.loads(f.read()))
    return tweetdf


def wordcountfile(filename):
	with open(filename,"r") as f:
		filetxt=f.read()
	wc=wordcount(filetxt.replace("\nENDOFTWEET\n","\n"))
	wcdf=pandas.DataFrame.from_dict(wc,orient="index").reset_index()
	wcdf=wcdf.rename(columns={'index':'word',0:'count'})
	return wcdf
	
def wordcountmulti(inpath,outpath,logger=xetrapal.astra.baselogger):
	for filename in os.listdir(inpath):
		logger.info("Working on file " + filename)
		wcdf=wordcountfile(os.path.join(inpath,filename))
		wcdf.to_csv(os.path.join(outpath,filename.rstrip(".txt")+"-wordcount.csv"),encoding="utf-8")
	


def dump_all_tweets_to_txt(persondf,outfile,logger=xetrapal.astra.baselogger):
	for person in persondf.screen_name:
		if os.path.exists(currworkingdir+"/"+person+".json"):
			tweetdf=pandas.read_json(currworkingdir+"/"+person+".json", orient="split")
			if "full_text" not in tweetdf.columns:
				continue
			for tweet in tweetdf.full_text:
				with open(outfile,"a") as f:
					f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")

def ngramcounternltk(series):
    word_vectorizer = CountVectorizer(ngram_range=(3,5), analyzer='word')
    sparse_matrix = word_vectorizer.fit_transform(series)
    frequencies=sum(sparse_matrix).toarray()[0] 
    freqdf=pandas.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['freq']).sort_values(by='freq')
    return freqdf
    
    
def tweet_cleaner(text):
    twitterhandlere=r'(@\w{1,15})\b'
    twitterhandle=re.compile(twitterhandlere)
    linkre= r'https?://[A-Za-z0-9./]+'
    link=re.compile(linkre)
    outtext=re.sub(twitterhandle,"",text)
    outtext=re.sub(link,"",outtext)
    return outtext

ananda=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
anandatw=ananda.get_twython()
anandagd=ananda.get_googledriver()
anandatweep=ananda.get_tweepy()
trollbaitsheet=anandagd.open_by_key(key="1zisiKnhF4cEW4H7fvhpZ7Y8cGfwQybvGgDg6Jnth5j4")
allusers=trollbaitsheet.worksheet_by_title("allusers").get_as_df()
men=trollbaitsheet.worksheet_by_title("men").get_as_df()
women=trollbaitsheet.worksheet_by_title("women").get_as_df() 

