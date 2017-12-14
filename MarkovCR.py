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

def loadTrain():
    trainSets = {}
    #init trainSets. 1st entry is author name.
    allUnique = []
    trainSets["Eddie_Izzard.txt"] = ["Izzard"]
    trainSets["Gabriel_Iglesias.txt"] = ["Iglesias"]
    trainSets["John_Mulaney.txt"] = ["Mulaney"]
    trainSets["Trevor_Noah.txt"] = ["Noah"]
    trainSets["Sarah_Silverman.txt"] = ["Silverman"]
    trainSets["Bo_Burnham.txt"] = ["Burnham"]
    trainSets["Hannibal_Buress.txt"] = ["Buress"]
    trainSets["Aziz_Ansari.txt"] = ["Ansari"]
    trainSets["Wanda_Sykes.txt"] = ["Sykes"]
 #   connect keys (fileNames) to processed list of words in file)
    for i in trainSets.keys():
        words = processFile(i)
        for w in words:
            trainSets[i].append(w)
            if w not in allUnique:
                allUnique.append(w)
    return trainSets, allUnique

def processFile(fileName):
    #load text file
    Text = open(fileName, mode = "r")
    wordlist = []
    #load list of stopwords (first list from https://www.ranks.nl/stopwords)
    stopWords = []
    stopFile = open("StopWords.txt", encoding = "utf-8", mode = "r")
    for word in stopFile:
        word = word.replace('\n', '')
        stopWords.append(word)
    #turn text into list of words
    for line in Text:
        line = line.replace('\n', '')
        line=line.replace('“','"')
        line=line.replace('”','"')
        line=line.replace("_","")
        line=line.replace("—"," ")
        listLine = line.split(' ')
        for w in listLine:
            w = "".join([ch for ch in w if ch not in string.punctuation]) # removing puncuation
            if w.lower() not in stopWords and len(w) > 0:
                tok = StemmingUtil.parseTokens(w)
                stem = StemmingUtil.createStems(tok)
                newstem=deepcopy(stem)
                for i in stem:
                    if i in punctuation:
                        newstem.remove(i)
                    if i in stopWords:
                        newstem.remove(i)
                wordlist.extend(newstem)
    return wordlist

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
    markov = MarkovChain(trainSets)
