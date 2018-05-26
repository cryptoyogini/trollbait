### GENERATE WORD-FREQUENCY MATRICES               
### author: Thiago Marzagao                        
### contact: marzagao ddott 1 at osu ddott edu                    

### supported encoding: UTF8                        
### supported character sets:
###     Basic Latin (Unicode 0-128)
###     Latin 1 Suplement (Unicode 129-255)
###     Latin Extended-A (Unicode 256-382)
import re
import collections


#ipath ='/home/lilhack110/wordcount/' # input folder
#opath = '/home/lilhack110/wordcount/' # output folder

# identify files to process
def analyze(rawText):
    #matches 30 reetitions or more of one character
    #regex2 = re.compile(u'(^.{30,})')
    #regex3 = re.compile(u'(\A\u002D)|(\u002D\Z)')
    
    # create dictionary to store word frequencies
    wordFreq = collections.Counter()
    
    # process each file chunk
   
    decodedText = rawText.decode('utf8').replace("\n"," ")
    # remove special characters and anything beyond Unicode 382
    #preCleanText = regex1.sub(' ', decodedText)
    # parse text
    parsedText = re.split(' ', decodedText)
    # clean up and count word
    if "" in parsedText:
        parsedText.remove("")
    for word in parsedText:
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
