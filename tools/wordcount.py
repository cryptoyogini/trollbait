### GENERATE WORD-FREQUENCY MATRICES               
### author: Thiago Marzagao                        
### contact: marzagao ddott 1 at osu ddott edu                    

### supported encoding: UTF8                        
### supported character sets:
###     Basic Latin (Unicode 0-128)
###     Latin 1 Suplement (Unicode 129-255)
###     Latin Extended-A (Unicode 256-382)

import os
import re
import sys
import collections


#ipath ='/home/lilhack110/wordcount/' # input folder
#opath = '/home/lilhack110/wordcount/' # output folder

# identify files to process
def wordcount(ipath,opath):
    done = set([file.replace('csv', 'txt') for file in os.listdir(opath) 
            if file[-3:] == 'csv'])
    filesToProcess = [file for file in os.listdir(ipath)
                  if file[-3:] == 'txt' if file not in done]
    totalFiles = len(filesToProcess)

    # quit if no files to process
    if totalFiles == 0:
        print 'No unprocessed txt files in %s' %ipath
        
    # map every uppercase character onto corresponding lowercase character
    
    # compile regular expressions
    regex2 = re.compile(u'(^.{30,})')
    regex3 = re.compile(u'(\A\u002D)|(\u002D\Z)')
    
    # process each file
    print ''
    fileNumber = 0
    for fileName in filesToProcess:
        if fileName[-3:] == 'txt': # discard non-txt files
            fileNumber += 1
    
            # monitor progress
            print 'Processing {} (file {} of {})'.format(fileName, 
                                                         fileNumber, 
                                                         totalFiles)
    
            # get file size and set chunk size
            chunkSize = 10000000 # number of bytes to process at a time
            fileSize = os.path.getsize(ipath + fileName)
            totalChunks = (fileSize / chunkSize) + 1 
                   
            # open file
            file = open(ipath + fileName, mode = 'r')
    
            # create dictionary to store word frequencies
            wordFreq = collections.Counter()
            
            # process each file chunk
            chunkNumber = 0
            while chunkNumber < totalChunks:
            
                # monitor progress
                chunkNumber += 1
                #sys.stdout.write('Processing chunk {} of {} \r'.format(chunkNumber, totalChunks))
                #sys.stdout.flush()
            
                # read text
                rawText = file.read(chunkSize)
            
                # don't split last word
                #separators = [' ', '\r', '\n']
                #if chunkNumber < totalChunks:
                #    while rawText[-1] not in separators:
                #        rawText = rawText + file.read(1)
                
                # decode text
                decodedText = rawText.decode('utf8')
                # remove special characters and anything beyond Unicode 382
                #preCleanText = regex1.sub(' ', decodedText)
               
                # parse text
                parsedText = re.split(' |--', decodedText)
                print "parsedtext",parsedText                   
                # clean up and count word
                for word in parsedText:
    
                    # if word > 30 characters, leave out
                    if regex2.search(word):
                        continue
    
                    # if word has trailing hyphens, fix
                    while regex3.search(word):
                        word = regex3.sub('', word)
                        
                    # if word is empty string, leave out
                    if word == '':
                        continue
    
                    # if word == proper noun, leave out
                   
    
                    # if word has uppercase, fix
                    
                    
                    # add word to count
                    wordFreq[word] += 1
                
            # create output file
            output = fileName.replace('txt', 'csv')
            output = open(opath + output, mode = 'w')
    
            # write to output file
            totalWords = sum(wordFreq.values())
            for word, absFreq in wordFreq.items():
                relFreq = float(absFreq) / totalWords
                output.write(word.encode('utf8') + ',' 
                             + str(absFreq) + ','
                             + str(relFreq) + '\n')
            output.close()
            print '\n{} successfully processed'.format(fileName)
            print ''
    
    # wrap up
    print 'Done! All files successfully processed'
    print 'Output saved to', opath
    print ''
