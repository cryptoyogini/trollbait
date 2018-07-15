import sys
sys.path.append("/opt/xetrapal")
import xetrapal
import tweepy
import pandas
import datetime
import math
import json
from sklearn.feature_extraction.text import CountVectorizer 

sys.path.append("/opt/livingdata/lib")


def get_twitter_ts(string):
    return datetime.datetime.strptime(string.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y")
    
def get_age(createdts):
    now=datetime.datetime.now()
    age=now-createdts
    return math.ceil(age.total_seconds()/3600)

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


ananda=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
anandatw=ananda.get_twython()
anandagd=ananda.get_googledriver()
twconfig=xetrapal.karma.get_section(ananda.config,"Twython")
tweep=get_tweepy(twconfig)
trollbaitsheet=anandagd.open_by_key(key="1zisiKnhF4cEW4H7fvhpZ7Y8cGfwQybvGgDg6Jnth5j4")


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

