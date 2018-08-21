%load_ext autoreload
%autoreload 2
%run xetrapalworkflow-ngram.py "/home/ananda/ab/xetrapal-data/trollbait1_2/"
womentweetseries
ngrammen=ngramcounter(mentweetseries)
ngrammen
ngrammen.to_csv("/home/ananda/mengram1000.csv",encoding="utf-8")
ngramwomen=ngramcounter(womentweetseries)
ngramwomen.to_csv("/home/ananda/womengram1000.csv",encoding="utf-8")
ngramwomen.columns
ngramwomen.reset_index()
ngramwomen=ngramwomen.reset_index()
ngrammen=ngrammen.reset_index()
ngrammen
ngrammen.columns
ngrammen=ngrammen.rename(columns={'index':'ngram'}
)
ngramwomen=ngramwomen.rename(columns={'index':'ngram'}
)
ngrammen.to_csv("/home/ananda/mengram1000.csv",encoding="utf-8")
ngramwomen.to_csv("/home/ananda/womengram1000.csv",encoding="utf-8")
for row in ngrammen.itertuples():
    print row[0]
    
    
    if row[0] in ngramwomen[ngramwomen.columns[0]].values:
        print row,common
        common.append(row)
for row in ngrammen.itertuples():
    print row[1]
    
    
    if row[1] in ngramwomen[ngramwomen.columns[0]].values:
        print row,common
        common.append(row)
common
common=pandas.DataFrame(columns=ngrammen.columns)
for row in ngrammen.itertuples():
    if row[1] in ngramwomen[ngramwomen.columns[0]].values:
        row['Common']=True;
        common.append(row)
ngramwomen.ngram.values
for row in ngrammen.itertuples():
    if row[1] in ngramwomen.ngram.values:
        row['Common']=True;
        common.append(row)
for row in tqdm(ngrammen.itertuples()):
    if row[1] in ngramwomen.ngram.values:
        row['Common']=True;
        common.append(row)
history
onlymengrams1000=pandas.DataFrame(columns=ngrammen.columns)
onlywomengrams1000=pandas.DataFrame(columns=ngramwomen.columns)
common=pandas.DataFrame(columns=ngrammen.columns)
for row in tqdm(ngrammen.itertuples()):
    if row['ngram'] in ngramwomen.ngram.values:
        common.append(row)
    else:
        onlymengrams1000.append(row)
for row in tqdm(ngrammen.itertuples()):
    if row[0] in ngramwomen.ngram.values:
        common.append(row)
    else:
        onlymengrams1000.append(row)
for row in tqdm(ngrammen.iteritems()):
    if row[0] in ngramwomen.ngram.values:
        common.append(row)
    else:
        onlymengrams1000.append(row)
for ngram in p[p.columns[0]]:
    #print ngram
    if ngram in q[q.columns[0]].values:
        print ngram, "Common"
    else:
        onlywomen.append(ngram)
p=ngrammen
p=ngramwomen
q=ngrammen
for ngram in p[p.columns[0]]:
    #print ngram
    if ngram in q[q.columns[0]].values:
        print ngram, "Common"
    else:
        onlywomen.append(ngram)
onlywomen=pandas.DataFrame(columns=p.columns)
for ngram in p[p.columns[0]]:
    #print ngram
    if ngram in q[q.columns[0]].values:
        print ngram, "Common"
    else:
        onlywomen.append(ngram)
p['Common']=p.ngram.progress_apply(lambda x: True if x in q['ngram'].values else False)
import tqdm
from tqdm import tqdm
tqdm.pandas()
p['Common']=p.ngram.progress_apply(lambda x: True if x in q['ngram'].values else False)
p=p[p.freq>10]
q=q[q.freq>10]
p
q
p['Common']=p.ngram.progress_apply(lambda x: True if x in q['ngram'].values else False)
p
q['Common']=q.ngram.progress_apply(lambda x: True if x in p['ngram'].values else False)
q
p[p.Common==True]
q[q.Common==True]
p[p.Common==True]
common =p[p.Common==True]
onlywomen=p[p.Common=False]
onlywomen=p[p.Common==False]
onlymen=q[q.Common==False]
onlymen.to_csv("/home/ananda/onlymenfreqs-1000-gt10.csv", encoding="utf-8")
onlywomen.to_csv("/home/ananda/onlywomenfreqs-1000-gt10.csv", encoding="utf-8")
%run xetrapalworkflow.py
%run xetrapalworkflow.py xx
onlywomengt10=trollbaitsheet.add_worksheet("1000-each-onlywomen-ngrams-freq-gt-10")
trollbaitsheet.add_worksheet("xx")
trollbaitsheet.add_worksheet("xx")
trollbaitsheet
trollbaitsheet.list_permissions
trollbaitsheet.list_permissions()
%run xetrapalworkflow.py xx
anandagd.create("Helloworld")
trollbaitsheet=anandagd.create("Trollbait Frequency Report")
onlywomengt10=trollbaitsheet.add_worksheet("1000-each-onlywomen-ngrams-freq-gt-10")
onlywomengt10.set_dataframe(onlywomen,(1,1))
onlymengt10=trollbaitsheet.add_worksheet("1000-each-onlymen-ngrams-freq-gt-10")
onlymengt10.set_dataframe(onlymen,(1,1))
commongt10=trollbaitsheet.add_worksheet("1000-each-common-ngrams-freq-gt-10")
commongt10.set_dataframe(common,(1,1))
cat /home/ananda/ab/ab.conf
trollbaitsheet.id
ls ~/ab
ls /home/ananda/ab/xetrapal-auth/
history

