#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
sys.path.append("/opt/xetrapal")
sys.path.append("../lib")
import xetrapal
import tweepy
import twython
import pandas
import datetime
import math
import json
import re,time
import nltk
import colored
from sklearn.feature_extraction.text import CountVectorizer 
from tqdm import tqdm
import collections
from tqdm import tqdm
tqdm.pandas()
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
    
    

def make_fasttext_training(df,outfile):
    texts = df.text.values
    cat_id = df.target.values
    with open(outfile, 'w') as f:
        for idx in range(df.__len__()):
            f.write('__label__' + str(cat_id[idx]) + ' ' + texts[idx].replace('\n', '') + '</s>\n')

def make_fasttext_input(df,fname):
    texts = df.text.values
#    cat_id = df.target.values
    with open(fname, 'w') as f:
        for idx in range(df.__len__()):
            f.write(texts[idx].replace('\n', '') + '</s>\n') 


def get_ft_labels(modelfile,infile,outfile):
    #print text
    label=os.system('fastText predict-prob %s %s > %s' %(modelfile,infile,outfile))
    with open(infile,"r") as f:
		inputtext=f.readlines()
	
    with open(outfile,"r") as f:
		outputlabels=f.readlines()
	
    inputseries=pandas.Series(inputtext)
    outputseries=pandas.Series(outputlabels)
    if len(inputseries)==len(outputseries):
		outdf=pandas.DataFrame(columns=['text','labels'])
		outdf['text']=inputseries
		outdf['labels']=outputseries.apply(lambda x: x.rstrip("\n"))
		return outdf
    else:
        return "Length Mismatch"
		
	
def ft_label_file(infile,modelfile,logger=xetrapal.astra.baselogger):
	with open(infile,"r") as f:
		intext=f.read()
	logger.info("Read file "+ infile)
	intextlist=intext.split("\nENDOFTWEET\n")
	if "" in intextlist:
		intextlist.remove("")
	intextdf=pandas.DataFrame(intextlist,columns=['text'])
	logger.info("Cleaning text")
	intextdf.text=intextdf.text.progress_apply(lambda x: tweet_cleaner(x))
	
#	logger.info("Dropping empty rows")
	#intextdf=intextdf[intextdf.text!=""].reset_index().drop("index",axis=1,inplace=True)
#	intextdf.text.apply(lambda x: x.replace('\n', '') + '</s>\n')
	#logger.info("Getting fasttext labels and probabilities")
	#intextdf['labelfull']=intextdf.text.progress_apply(lambda x: get_ft_label(x,modelfile))
	#logger.info("Splitting the label and probability")
	#intextdf['label']=intextdf.text.progress_apply(lambda x: x.split(" ")[0])
	#intextdf['probability']=intextdf.text.progress_apply(lambda x: x.split(" ")[1])
	#intextdf.drop(["labelfull"],axis=1,inplace=True)	
	#logger.info("Returning the final df")
	#return intextdf
	return intextdf

def ft_label_multi(inpath,outpath,modelfile,logger=xetrapal.astra.baselogger):
	for filename in os.listdir(inpath):
		outfilename=os.path.join(outpath,filename.rstrip(".txt")+"-ftlabels-"+os.path.split(modelfile)[1].replace(".bin","")+".csv")
		logger.info("Getting FT labels for file " + filename +". Output to "+ outfilename)
		ftdf=ft_label_file(os.path.join(inpath,filename),modelfile,logger=logger)
		if ftdf != "Length Mismatch":
			ftdf.to_csv(outfilename,encoding="utf-8")
        else:
			logger.error("Length mismatch in file "+ filename)


def ngramfrequencyht(filename,gramlength=3,logger=xetrapal.astra.baselogger):
    with open(filename,"r") as f:
        intext=f.read()
    logger.info("Read file "+ filename)   
    logger.info("Cleaning text")
    cleantext=intext.replace("\nENDOFTWEET\n","\n")
    cleantext=cleantext.lower()
    cleantext=tweet_cleaner(cleantext)
    cleantext=re.sub("\ +"," ",cleantext)
    logger.info("Tokenizing input")
    t=Tokenizer(cleantext)
    t.tokenize()
    grams=nltk.ngrams(t.tokens,gramlength)
    logger.info("Generating freq distribution")
    fdist=nltk.FreqDist(grams)
    freqdist={}
    for k,v in fdist.items():
        freqdist[" ".join(k)]=v
    logger.info("Returning final values")
    freqdistdf=pandas.Series(freqdist).to_frame()
    return freqdistdf

def get_ngrams(inpath,outpath,gramlength=3,logger=xetrapal.astra.baselogger):
	for filename in os.listdir(inpath):
		outfilename=os.path.join(outpath,filename.rstrip(".txt")+"-"+str(gramlength)+"grams.csv")
		logger.info("Getting ngrams for file " + filename +". Output to "+ outfilename)
		ftdf=ngramfrequencyht(os.path.join(inpath,filename),gramlength,logger=logger)
		ftdf.to_csv(outfilename,encoding="utf-8")
	
	
def hasmarker(text,markerlist):
	for marker in markerlist:
		if marker in text.lower():
			return marker
	return None

def tweet_cleaner(text):
    twitterhandlere=r'(@\w{1,15})\b'
    twitterhandle=re.compile(twitterhandlere)
    linkre= r'https?://[A-Za-z0-9./]+'
    link=re.compile(linkre)
    outtext=re.sub(link,"",text)
    #outtext=re.sub(twitterhandle,"",outtext)
    outtext=re.sub('[\"\&\;\(\)\`]+',"",outtext)
    outtext=re.sub('RT\s+',"",outtext)
    outtext=re.sub(ur'…+',"",outtext)
    outtext=re.sub('\.\.+',".",outtext)
    outtext=re.sub('\s+'," ",outtext)
    outtext=re.sub(':\s+'," ",outtext)
    outtext=re.sub('\samp\s'," and ",outtext)
    outtext=outtext.lstrip(" ").rstrip(" ")
    return outtext



class XpalTrollTracker(twython.TwythonStreamer):
    def __init__(self,ofile,markersheet,logger,*args, **kwargs):
        super(XpalTrollTracker,self).__init__(*args, **kwargs)
        self.ofile=ofile
        self.buffer=[]
        self.logger=logger
        self.markersheet=markersheet
        self.markerlist=update_profanity(self.markersheet)
        
    def on_success(self, data):
		if 'text' in data.keys():
			#self.logger.info(data['text'])
			cleantext=tweet_cleaner(data['text'])
			self.logger.info(cleantext)
			marker=hasmarker(cleantext,self.markerlist)
			if marker!=None:
				self.logger.info("Caught troll with marker " + marker)
				with open(self.ofile,"a") as f:
					f.write("__label__troll "+cleantext.encode("utf-8").replace("\n"," ").lower()+"</s>\n")
				with open("/home/ananda/trolls.txt","a") as f:
					f.write(str(data['user']['screen_name'])+"\n")
				self.logger.info("Updating profanity list")	
				self.markerlist=update_profanity(self.markersheet)
			
			else:
				with open(self.ofile,"a") as f:
					if cleantext.replace(" ","")!="":
						f.write("__label__nomarker "+cleantext.encode("utf-8").replace("\n"," ").lower()+"</s>\n")
		time.sleep(0.1)
			
    def on_error(self, status_code, data):
        print(status_code)

def get_troll_tracker(config,ofilename=None,markersheet=None,logger=xetrapal.astra.baselogger):
    
    if ofilename==None:
        ts=datetime.now()
        ofilename="/tmp/TwythonStreamer-"+ts.strftime("%Y%b%d-%H%M%S"+".json")
    logger.info("Trying to get a twython streamer to work with twitter streams")
    app_key=config.get("Twython",'app_key')
    app_secret=config.get("Twython",'app_secret')
    oauth_token=config.get("Twython",'oauth_token')
    oauth_token_secret=config.get("Twython",'oauth_token_secret')
    try:
        t=XpalTrollTracker(ofilename,markersheet,logger,app_key,app_secret,oauth_token,oauth_token_secret)
        logger.info("Streamer logging at "  + colored.stylize(t.ofile,colored.fg("yellow")))
        return t
    except Exception as e:
		logger.error("Could not get twython streamer because %s" %repr(e))
		return None
	
	


#ananda=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
#anandatw=ananda.get_twython()
#anandagd=ananda.get_googledriver()
#anandatweep=ananda.get_tweepy()
#trollbaitsheet=anandagd.open_by_key(key="1zisiKnhF4cEW4H7fvhpZ7Y8cGfwQybvGgDg6Jnth5j4")
#allusers=trollbaitsheet.worksheet_by_title("allusers").get_as_df()
#men=trollbaitsheet.worksheet_by_title("men").get_as_df()
#women=trollbaitsheet.worksheet_by_title("women").get_as_df() 
#trainsheet=anandagd.open_by_key("1FRE-7UFoQN0V0qqaRCeMTkNWDxKpYYZuJqRi5TLUQf4")
#pls=trainsheet.worksheet_by_title("profanitylist")
#pl=pls.get_as_df()
#pl=pl.drop_duplicates()
#profanitylist=pl.phrase

def start_trollbait(xpal,pls):
	#profanitylist=update_profanity(pls)
	while True:
		try:
			trolltracker=get_troll_tracker(xpal.config,ofilename="/home/ananda/trolltrain2018-08-26-stream.txt",markersheet=pls,logger=xpal.logger)
			trolltracker.statuses.filter(track="india,indian,desi,jnu,media,politics,right wing,left wing,kerala,beef,hindutva,communism,homosexuality,gauraksha,feminist,feminazi,kerala,floods,allah,pakistan,bangladesh,bharat,hindu,muslim,kashmir,conversion,arnab goswami,india news,aadhaar,भारत,हिंदू,मुसल्मान,आधार,shehla rashid,arundhati roy,umar khalid,तीन-तलाक,maoist,naxal,adivasi,anti-sikh riots,1984")
		except Exception as e:
			print "Restarting ..."+repr(e)
			if os.path.exists("/home/ananda/stopper"):
				break;
		
def update_profanity(pls):
    pl=pls.get_as_df()
    pl=pl.drop_duplicates()
    profanitylist=pl.phrase
    return profanitylist
