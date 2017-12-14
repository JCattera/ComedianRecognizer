#MarkovCR
#
#Marina, Jamie, Matana

import sys
import StemmingUtil
import math
import string
from copy import deepcopy

punctuation=['!','``','\'\'','#','$','%','&','\'','(',')','*','+',',','-','--','.','/',':',';',\
'<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~','“','”','"']

def processFileTest():
    #load text file
    Text = open("TestSet_Passages.txt", mode = "r")
    testDict = {} 
    #load list of stopwords (first list from https://www.ranks.nl/stopwords)
    stopWords = []
    stopFile = open("StopWords.txt", encoding = "utf-8", mode = "r")
    for word in stopFile:
        word = word.replace('\n', '')
        stopWords.append(word)
    #create a dictionary where authors are keys and values are a list of their
        #5 passages
    done = False
    for line in Text:
        #read line after "###" as the author
        if "#" in line:
            author = Text.readline()
            author = author.replace('\n', ' ')
            continue
        else:
            #create a list of stems in passage
            passage = []
            line = line.replace('\n', ' ')
            line=line.replace('“','"')
            line=line.replace('”','"')            
            listLine = line.split(' ')
            for w in listLine:
                if w.lower() not in stopWords and w != "#" and w != '':
                    tok = StemmingUtil.parseTokens(w)
                    stem = StemmingUtil.createStems(tok)
                    newstem=deepcopy(stem)
                    for i in stem:
                            #print(i)
                        if i in punctuation:
                            newstem.remove(i)
                        if i in stopWords:
                           newstem.remove(i)
                    passage.extend(newstem)
            #add passage to appropriate author in the dictionary
            if author not in testDict.keys():
                testDict[author] =[passage]
            else:
                testDict.get(author).append(passage)
    return testDict


def main():
    #load train and test set files
    testSet = processFileTest()
    trainSets, allUnique = loadTrain()
