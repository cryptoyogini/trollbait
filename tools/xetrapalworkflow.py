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


#To move into Xetrapal
def get_twitter_ts(string):
    return datetime.datetime.strptime(string.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y")

#To move into Xetrapal
def get_age(createdts):
    now=datetime.datetime.now()
    age=now-createdts
    return math.ceil(age.total_seconds()/3600)

#To =move into Xetrapal
def get_mention_density(tw,screen_name,logger=xetrapal.astra.baselogger):
    last100=xetrapal.twkarmas.twython_get_ntweets_for_search(tw,"@"+screen_name,tcount=100)
    last100=pandas.DataFrame(last100)
    if "created_at" in last100.columns:
        #last100['createdts']=last100.created_at.apply(lambda x:datetime.datetime.strptime(x.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y"))
        last100['createdts']=last100.created_at.apply(get_twitter_ts)
        #m=last100.createdts.max()-last100.createdts.min()
        if len(last100)<100:
            logger.info("Account "+screen_name+" has less than 100 mentions")
        else:
            logger.info("Account "+screen_name+" has more than 100 mentions")
        logger.info("Calculating density as number of mentions divided by  hours since oldest mention or 100th oldest mention")
        m=get_age(last100.createdts.min())
        density=len(last100)/m
        return round(density,3)
    else:
        return 0
    
#To move into Xetrapal
def get_tweet_density(tw,screen_name,logger=xetrapal.astra.baselogger):
    last100=tw.get_user_timeline(screen_name=screen_name,count=100)
    last100=pandas.DataFrame(last100)
    if "created_at" in last100.columns:
        #last100['createdts']=last100.created_at.apply(lambda x:datetime.datetime.strptime(x.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y"))
        last100['createdts']=last100.created_at.apply(get_twitter_ts)
        #m=last100.createdts.max()-last100.createdts.min()
        if len(last100)<100:
            logger.info("Account "+screen_name+" has less than 100 tweets")
        else:
            logger.info("Account "+screen_name+" has more than 100 mentions")
        logger.info("Calculating density as number of tweets divided or 100 by hours since oldest tweet or 100th oldest tweet")
        m=get_age(last100.createdts.min())
        density=len(last100)/m
        return round(density,3)
    else:
        return 0

#To move into Xetrapal
def get_tweepy(twconfig,logger=xetrapal.astra.baselogger):
    app_key=twconfig.get("Twython",'app_key')
    app_secret=twconfig.get("Twython",'app_secret')
    oauth_token=twconfig.get("Twython",'oauth_token')
    oauth_token_secret=twconfig.get("Twython",'oauth_token_secret')
    auth=tweepy.OAuthHandler(app_key,app_secret)
    auth.set_access_token(oauth_token,oauth_token_secret)
    tweep=tweepy.API(auth)
    return tweep


def build_userdf(tweep,userlist,logger=xetrapal.astra.baselogger):
    users=[]
    logger.info("Getting list with owner unessentialist, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"unessentialist","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner arunram, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"arunram","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner brunogarcez, slug top-indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"brunogarcez","top-indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner edelman_india, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"edelman_india","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner ingridtherwath, slug india-journalists")
    for member in tweepy.Cursor(tweep.list_members,"ingridtherwath","india-journalists").items():
        users.append(member)
    logger.info("Getting users for added list")
    for name in userlist:
        try:
            users.append(tweep.get_user(screen_name=name))
        except:
            print name, "Oops!"
    userjson=[]
    for user in users:
        userjson.append(user._json)
    p=pandas.DataFrame(userjson)
    p=p.drop_duplicates(subset=['screen_name'])
    return p    

def ngramcounter(series):
    word_vectorizer = CountVectorizer(ngram_range=(1,5), analyzer='word')
    sparse_matrix = word_vectorizer.fit_transform(series)
    frequencies=sum(sparse_matrix).toarray()[0] 
    freqdf=pandas.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['freq']).sort_values(by='freq')
    return freqdf

def get_n_mentions(tw,persondf,count,path,logger=xetrapal.astra.baselogger):
    for person in tqdm(persondf.itertuples(),position=1):
        if  allusers.loc[allusers.screen_name==person.screen_name,'gotmentions'].item()=="":
            logger.info("Getting 1000 mentions or max for "+person.screen_name)
            last1000=xetrapal.twkarmas.twython_get_ntweets_for_search(tw,"@"+person.screen_name,logger=logger,tcount=count)
            try:
                last1000.to_json(os.path.join(path,person.screen_name+".json"),orient="split")
                #with open("/home/ananda/ab/xetrapal-data/trollbait1_1/"+person.screen_name+".json","w") as f:
                #    f.write(json.dumps(last1000.to_json(orient="split")))
                logger.info("Wrote file /home/ananda/ab/xetrapal-data/trollbait1_1/"+person.screen_name+".json")
                allusers.loc[allusers.screen_name==person.screen_name,'gotmentions']=True
                allusers.loc[allusers.screen_name==person.screen_name,'nummentions']=len(last1000)
                update_sheet()
            except Exception as e:
                logger.error("Could not write file /home/ananda/ab/xetrapal-data/trollbait1_1/"+person.screen_name+".json because "+repr(e))
        else:
            logger.info(person.screen_name+" already done cause "+ person.gotmentions)
        

def update_sheet():
    trollbaitsheet.worksheet_by_title("allusers").set_dataframe(allusers,(1,1))
    
def get_mentions(count,path):
    anandakarta=ananda.start_pykka_karta()
    anandakarta2=ananda.start_pykka_karta()
    anandakarta.tell({'msg':'run','func':get_n_mentions,'args':[anandatw,men,count,path],'kwargs':{"logger":ananda.logger}})
    anandakarta2.tell({'msg':'run','func':get_n_mentions,'args':[anandatw,women,count,path],'kwargs':{"logger":ananda.logger}})


def get_ngrams():
    anandakarta3=ananda.start_pykka_karta()
    anandakarta4=ananda.start_pykka_karta()
    anandakarta3.tell({'msg':'run','func':get_ngram_freq,'args':[men],'kwargs':{"logger":ananda.logger}})
    anandakarta4.tell({'msg':'run','func':get_ngram_freq,'args':[women],'kwargs':{"logger":ananda.logger}})

def get_ngram_freq(persondf,logger=xetrapal.astra.baselogger):
    for person in tqdm(persondf.screen_name,position=2,desc="Getting Ngrams"):
        tweetdf=pandas.read_json("/home/ananda/ab/xetrapal-data/trollbait1_1/"+person+".json",orient="split")
        if "full_text" in tweetdf.columns:
            p=ngramcounter(tweetdf.full_text)
            p.to_csv(os.path.join("/home/ananda/ab/xetrapal-data/trollbait1_1/",person+"-freq.csv"),encoding="utf-8")
        else:
            continue
        

def wordcount(text,logger=xetrapal.astra.baselogger):
    #matches 30 reetitions or more of one character
    #regex2 = re.compile(u'(^.{30,})')
    #regex3 = re.compile(u'(\A\u002D)|(\u002D\Z)')
    
    # create dictionary to store word frequencies
    wordFreq = collections.Counter()
    
    # process each file chunk
   
    
    # remove special characters and anything beyond Unicode 382
    #preCleanText = regex1.sub(' ', decodedText)
    # parse text
    #parsedText = re.split(' ', text)
    t=Tokenizer(text)
    logger.info("Beginning generate word count on input")
    logger.info("Tokenizing the input")
    t.tokenize()
    parsedText = t.tokens
    
    # clean up and count word
    while "" in parsedText:
        parsedText.remove("")
    for word in tqdm(parsedText):
        # if word > 30 characters, leave out
     #   if regex2.search(word):
           # continue
        # if word has trailing hyphens, fix
      #  while regex3.search(word):
      #     word = regex3.sub('', word)
            
        # if word is empty string, leave out
        if word == '':
            continue
        # add word to count
        wordFreq[word] += 1
    
    return wordFreq

ananda=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
anandatw=ananda.get_twython()
anandagd=ananda.get_googledriver()
anandatweep=ananda.get_tweepy()
twconfig=xetrapal.karma.get_section(ananda.config,"Twython")
tweep=get_tweepy(twconfig)
trollbaitsheet=anandagd.open_by_key(key="1zisiKnhF4cEW4H7fvhpZ7Y8cGfwQybvGgDg6Jnth5j4")
allusers=trollbaitsheet.worksheet_by_title("allusers").get_as_df()
men=trollbaitsheet.worksheet_by_title("men").get_as_df()
women=trollbaitsheet.worksheet_by_title("women").get_as_df() 




'''
p=build_userdf(tweep,userlist)
men=trollbaitsheet.worksheet_by_title("men")
women=trollbaitsheet.worksheet_by_title("women")
men =men.get_as_df()
women=women.get_as_df()
for woman in women.screen_name:
    last500=xetrapal.twkarmas.twython_get_ntweets_for_search(anandatw,"@"+woman,logger=ananda.logger,tcount=500)
    with open("/home/arjun/av//xetrapal-data/trollbait1_1/"+woman+".json","w") as f:
        f.write(json.dumps(last500))

for man in men.screen_name:
    last500=xetrapal.twkarmas.twython_get_ntweets_for_search(anandatw,"@"+man,logger=ananda.logger,tcount=500)
    with open("/home/ananda/ab/xetrapal-data/trollbait1_0/"+man+".json","w") as f:
        f.write(json.dump(last500))
'''
def load_tweets_from_json(filename):
    print filename
    with open(filename,"r") as f:
        tweetdf=pandas.DataFrame(json.loads(f.read()))
    return tweetdf

