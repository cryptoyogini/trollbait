%run xetrapalworkflow-final.py
logger=ananda.logger
logger.info("Starting analysis")
clear
logger.info("First we get the set of known victims and put their tweets into text files")
logger.info("Known victims : @Shehla_Rashid, @KunalKamra88, @UmarKhalidJNU, @kanhaiyakumar")
logger.info("Looking at 1000 tweets per victim")
shehlatweets1000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/shehlatweets5000.csv")
len(shehlatweets1000)
shehlatweets1000.created_at
shehlatweets1000[:1000]
shehlatweets1000[:1000].created_at
shehlatweets1000[:1000].created_at
shehlatweets1000=shehlatweets1000[:1000]
kunaltweets1000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/kunaltweets5000.csv")[:1000]
kunaltweets1000
kunaltweets1000.created_at
umartweets1000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/umartweets5000.csv")[:1000]
kanhaiyatweets1000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/kanhaiyatweets5000.csv")[:1000]
kanhaiyatweets1000
kanhaiyatweets1000.created_at
logger.info("Cleaning tweets to remove twitter user handles")
shehlatweets1000nohandle = shehlatweets1000.full_text.apply(lambda x: re.sub(twitterhandle,"",x))
import re
twitterhandlere=r'(@\w{1,15})\b'

twitterhandle=re.compile(twitterhandlere)
shehlatweets1000nohandle = shehlatweets1000.full_text.apply(lambda x: re.sub(twitterhandle,"",x))
kunaltweets1000nohandle = kunaltweets1000.full_text.apply(lambda x: re.sub(twitterhandle,"",x))
umartweets1000nohandle = umartweets1000.full_text.apply(lambda x: re.sub(twitterhandle,"",x))
kanhaiyatweets1000nohandle = kanhaiyatweets1000.full_text.apply(lambda x: re.sub(twitterhandle,"",x))
kanhaiyatweets1000nohandle
kanhaiyatweets1000nohandle['...' in kanhaiyatweets1000nohandle[0]]
def tweet_cleaner(text):
    twitterhandlere=r'(@\w{1,15})\b'
    twitterhandle=re.compile(twitterhandlere)
    linkre= r'https?://[A-Za-z0-9./]+'
    link=re.compile(linkre)
    outtext=text.replace(twitterhandle,"",text)
    outtext=outtext.replace(link,"",text)
    return outtext
kanhaiyatweets1000.full_text.apply(tweet_cleaner)
def tweet_cleaner(text):
    twitterhandlere=r'(@\w{1,15})\b'
    twitterhandle=re.compile(twitterhandlere)
    linkre= r'https?://[A-Za-z0-9./]+'
    link=re.compile(linkre)
    outtext=re.sub(twitterhandle,"",text)
    outtext=re.sub(link,"",outtext)
    return outtext
kanhaiyatweets1000.full_text.apply(tweet_cleaner)
kanhaiyatweets1000.full_text.apply(tweet_cleaner).drop_duplicates()
kanhaiyacleantweets1000=kanhaiyatweets1000.full_text.apply(tweet_cleaner).drop_duplicates()
shehlacleantweets1000=shehlatweets1000.full_text.apply(tweet_cleaner).drop_duplicates()
kunalcleantweets1000=kunaltweets1000.full_text.apply(tweet_cleaner).drop_duplicates()
umarcleantweets1000=umartweets1000.full_text.apply(tweet_cleaner).drop_duplicates()
kanhaiyacleantweets1000
umarcleantweets1000
shehlacleantweets1000
kunalcleantweets1000
logger.info("Cleaned tweets to remove twitter user handles")
logger.info("Cleaned tweets to remove twitter user handles, links and duplicates after removal")
for tweet in shehlacleantweets1000:
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets1000.txt","a") as f:
        f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
for tweet in shehlacleantweets1000:
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets1000.txt","a") as f:
        f.write(tweet.decode("utf-8")+"\nENDOFTWEET\n")
for tweet in shehlacleantweets1000:
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets1000.txt","a") as f:
        f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
for tweet in shehlacleantweets1000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets1000.txt","a") as f:
        f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
shehlacleantweets1000
for tweet in shehlacleantweets1000:
    print tweet.encode("utf-8")
for tweet in shehlacleantweets1000:
    print tweet
for tweet in shehlacleantweets1000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets1000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
len(shehlacleantweets1000
)
logger.info("Saving Cleaned tweets to a text file with ENDOFTWEET as a delimiter")
for tweet in kunalcleantweets1000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/kunalcleantweets1000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
for tweet in kanhaiyacleantweets1000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/kanhaiyacleantweets1000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
for tweet in umarcleantweets1000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/umarcleantweets1000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
len(umarcleantweets1000)
len(kunalcleantweets1000)
len(kanhaiyacleantweets1000)
logger.info("Consolidating men tweets into a single dataframe")
for man in men.screen_name:
    if os.path.exists(currworkingdir+"/"+man+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+man+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        for tweet in tweetdf.full_text:
            with open("/home/ananda/mentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
currworkingdir="/home/ananda/trollbaitdata/trollbait1000/"
for man in men.screen_name:
    logger.info("Getting tweets for %s from json file" %man)
    if os.path.exists(currworkingdir+"/"+man+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+man+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        logger.info("Cleaning %s's tweets" %man)
        tweetdf.full_text=tweetdf.full_text.apply(tweet_cleaner)
        logger.info("Saving tweets for %s to file /home/ananda/trollbaitpass2/txt/mentweets1000.txt" %man)
        for tweet in tweetdf.full_text:
            with open("/home/ananda/trollbaitpass2/txt/mentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
logger.info("Consolidating women tweets into a single dataframe")
for woman in women.screen_name:
    logger.info("Getting tweets for %s from json file" %man)
    if os.path.exists(currworkingdir+"/"+woman+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+woman+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        logger.info("Cleaning %s's tweets" %woman)
        tweetdf.full_text=tweetdf.full_text.apply(tweet_cleaner)
        logger.info("Saving tweets for %s to file /home/ananda/trollbaitpass2/txt/womentweets1000.txt" %woman)
        for tweet in tweetdf.full_text:
            with open("/home/ananda/trollbaitpass2/txt/womentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
logger.warning("Fixing last pass, removing file")
rm /home/ananda/trollbaitpass2/txt/womentweets1000.txt
for woman in women.screen_name:
    logger.info("Getting tweets for %s from json file" %woman)
    if os.path.exists(currworkingdir+"/"+woman+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+woman+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        logger.info("Cleaning %s's tweets" %woman)
        tweetdf.full_text=tweetdf.full_text.apply(tweet_cleaner)
        logger.info("Saving tweets for %s to file /home/ananda/trollbaitpass2/txt/womentweets1000.txt" %woman)
        for tweet in tweetdf.full_text:
            with open("/home/ananda/trollbaitpass2/txt/womentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
logger.warning("Last pass didnt remove dupes, fixing and redoing")
rm /home/ananda/trollbaitpass2/txt/womentweets1000.txt
rm /home/ananda/trollbaitpass2/txt/mentweets1000.txt
for woman in women.screen_name:
    logger.info("Getting tweets for %s from json file" %woman)
    if os.path.exists(currworkingdir+"/"+woman+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+woman+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        logger.info("Cleaning %s's tweets" %woman)
        tweets=tweetdf.full_text.apply(tweet_cleaner).drop_duplicates()
        logger.info("Saving tweets for %s to file /home/ananda/trollbaitpass2/txt/womentweets1000.txt" %woman)
        for tweet in tweets:
            with open("/home/ananda/trollbaitpass2/txt/womentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
for man in men.screen_name:
    logger.info("Getting tweets for %s from json file" %man)
    if os.path.exists(currworkingdir+"/"+man+".json"):
        tweetdf=pandas.read_json(currworkingdir+"/"+man+".json", orient="split")
        if "full_text" not in tweetdf.columns:
            continue
        logger.info("Cleaning %s's tweets" %man)
        tweets=tweetdf.full_text.apply(tweet_cleaner).drop_duplicates()
        logger.info("Saving tweets for %s to file /home/ananda/trollbaitpass2/txt/mentweets1000.txt" %man)
        for tweet in tweets:
            with open("/home/ananda/trollbaitpass2/txt/mentweets1000.txt","a") as f:
                f.write(tweet.encode("utf-8")+"\nENDOFTWEET\n")
clear
logger.warning("Renaming mentweets1000.txt to mentweets1000clean.txt")
logger.warning("Renaming womentweets1000.txt to womentweets1000clean.txt")
mv /home/ananda/trollbaitpass2/txt/mentweets1000.txt /home/ananda/trollbaitpass2/txt/mentweets1000clean.txt
mv /home/ananda/trollbaitpass2/txt/womentweets1000.txt /home/ananda/trollbaitpass2/txt/womentweets1000clean.txt
mv /home/ananda/trollbaitpass2/txt/mentweets1000clean.txt /home/ananda/trollbaitpass2/txt/mencleantweets1000.txt
mv /home/ananda/trollbaitpass2/txt/womentweets1000clean.txt /home/ananda/trollbaitpass2/txt/womencleantweets1000.txt

shehlatweets5000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/shehlatweets5000.csv")
kunaltweets5000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/kunaltweets5000.csv")
umartweets5000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/umartweets5000.csv")
kanhaiyatweets5000=pandas.read_csv("/home/ananda/trollbaitdata/useful/csv/kanhaiyatweets5000.csv")
shehlacleantweets5000=shehlatweets5000.full_text.apply(tweet_cleaner).drop_duplicates()
umarcleantweets5000=umartweets5000.full_text.apply(tweet_cleaner).drop_duplicates()
kunalcleantweets5000=kunaltweets5000.full_text.apply(tweet_cleaner).drop_duplicates()
kanhaiyacleantweets5000=kanhaiyatweets5000.full_text.apply(tweet_cleaner).drop_duplicates()
logger.info("Repeating the same for 5000 tweets for the known victims to build a training model plus for extended testing later")
for tweet in umarcleantweets5000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/umarcleantweets5000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
for tweet in shehlacleantweets5000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/shehlacleantweets5000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
for tweet in kunalcleantweets5000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/kunalcleantweets5000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
for tweet in kanhaiyacleantweets5000:
    print tweet
    with open("/home/ananda/trollbaitpass2/txt/kanhaiyacleantweets5000.txt","a") as f:
        f.write(tweet+"\nENDOFTWEET\n")
len(shehlacleantweets5000)
len(kunalcleantweets5000)
len(kanhaiyacleantweets5000)
len(uumarcleantweets5000)
len(umarcleantweets5000)
