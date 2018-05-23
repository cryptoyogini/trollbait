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

ipath ='/home/lilhack110/wordcount/' # input folder
opath = '/home/lilhack110/wordcount/' # output folder

# identify files to process
done = set([file.replace('csv', 'txt') for file in os.listdir(opath) 
            if file[-3:] == 'csv'])
filesToProcess = [file for file in os.listdir(ipath)
                  if file[-3:] == 'txt' if file not in done]
totalFiles = len(filesToProcess)

# quit if no files to process
if totalFiles == 0:
    sys.exit('No unprocessed txt files in {}'.format(ipath))
    
# map every uppercase character onto corresponding lowercase character

# compile regular expressions
upperList = u'\u0041-\u005A\u00C0-\u00D6\u00D8-\u00DE\u0100\u0102\u0104\
              \u0106\u0108\u010A\u010C\u010E\u0110\u0112\u0114\u0116\u0118\
              \u011A\u011C\u011E\u0120\u0122\u0124\u0126\u0128\u012A\u012C\
              \u012E\u0130\u0132\u0134\u0136\u0139\u013B\u013D\u013F\u0141\
              \u0143\u0145\u0147\u014A\u014C\u014E\u0150\u0152\u0154\u0156\
              \u0158\u015A\u015C\u015E\u0160\u0162\u0164\u0166\u0168\u016A\
              \u016C\u016E\u0170\u0172\u0174\u0176\u0178\u0179\u017B\u017D\u0900-\u097F'
regex1 = re.compile(u'[^\u0041-\u005A\u0061-\u007A\u00C0-\u00D6\u00D8-\u00F6\
                    \u00F8-\u00FF\u0100-\u017F\u0020\u002D]')
regex2 = re.compile(u'(^.{30,})')
regex3 = re.compile(u'(\A\u002D)|(\u002D\Z)')
regex4 = re.compile(ur'\A[{}]'.format(upperList))
regex5 = re.compile(ur'(?P<char>[{}])'.format(upperList))

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
            sys.stdout.write('Processing chunk {} of {} \r'
                             .format(chunkNumber, totalChunks))
            sys.stdout.flush()
        
            # read text
            rawText = file.read(chunkSize)
        
            # don't split last word
            separators = [' ', '\r', '\n']
            if chunkNumber < totalChunks:
                while rawText[-1] not in separators:
                    rawText = rawText + file.read(1)
            
            # decode text
            decodedText = rawText.decode('utf8')
            preCleanText = regex1.sub(' ', decodedText)
            # remove special characters and anything beyond Unicode 382
            #preCleanText = regex1.sub(' ', decodedText)
           
            # parse text
            parsedText = re.split(' |--', decodedText)
            print "parsedtext",parsedText                   
            # clean up and count word
            uniques = set(parsedText)
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
