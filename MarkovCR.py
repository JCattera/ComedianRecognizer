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
    trainSets = {} #list of text file names
    markovChain = {} #triple-nested dictionary for markov chain
    #init trainSets. 1st entry is author name.
    allUnique = []
    trainSets["Izzard"] = "Eddie_Izzard.txt"
    trainSets["Iglesias"] = "Gabriel_Iglesias.txt"
    trainSets["Mulaney"] = "John_Mulaney.txt"
    trainSets["Noah"] = "Trevor_Noah.txt"
    trainSets["Silverman"] = "Sarah_Silverman.txt"
    trainSets["Burnham"] = "Bo_Burnham.txt"
    trainSets["Buress"] = "Hannibal_Buress.txt"
    trainSets["Ansari"] = "Aziz_Ansari.txt"
    trainSets["Sykes"] = "Wanda_Sykes.txt"
 #   connect keys (fileNames) to processed list of words in file)
    for comic in ["Mulaney"]:
        #enter 1st nest of markovChain dictionary (comedians)
        comicChain = processFile(trainSets.get(comic), comicChain = {})
        markovChain[comic] = comicChain
    return markovChain

def processFile(fileName, comicChain):
    #load text file
    Text = open(fileName, encoding = "utf-8", mode = "r")
##    #load list of stopwords (first list from https://www.ranks.nl/stopwords)
##    stopWords = []
##    stopFile = open("StopWords.txt", encoding = "utf-8", mode = "r")
##    for word in stopFile:
##        word = word.replace('\n', '')
##        stopWords.append(word)
    #turn line of text into list of words
    prevW = ""
    currentW = ""
    for line in Text:
        line = line.replace('\n', '')
        line=line.replace('“','"')
        line=line.replace('”','"')
        line=line.replace("_","")
        line=line.replace("—"," ")
        listLine = line.split(' ')
        for w in listLine:
            w = "".join([ch for ch in w if ch not in string.punctuation]) # removing puncuation
            #enter 2nd nest of markovChain dictionary (root word)
            if prevW != "":
                currentW = w
                #enter 3rd nest of markovChain dictionary (word given root word)
                if prevW in comicChain.keys():
                    givenWordDict = {}
                    givenWordDict = comicChain.get(prevW)
                    #count the # of times current word appears given previous word
                    if currentW not in givenWordDict.keys():
                        givenWordDict[currentW] = 1 
                    else:
                        givenWordDict[currentW] += 1
                else:
                    comicChain[prevW] = {}
                    givenWordDict = comicChain.get(prevW)
                    givenWordDict[currentW] = 1
            prevW = w
    return comicChain

def processFileTest():
    #load text file
    Text = open("TestSet_Passages.txt", encoding = "utf-8", mode = "r")
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

            #add passage to appropriate author in the dictionary
            if author not in testDict.keys():
                testDict[author] =[passage]
            else:
                testDict.get(author).append(passage)
    return testDict


def probability(markovChain):
    for comic in markovChain.keys():
        comicChain = markovChain.get(comic)
        for word1 in comicChain.keys():
            word1Dict = comicChain.get(word1)
            #find total number of times word1 has appeared in text
            totalW = 0
            for word2 in word1Dict.keys():
                totalW += word1Dict.get(word2)
            for word2 in word1Dict.keys():
                word1Dict[word2] = word1Dict.get(word2) / totalW
                print(word1, ":", word2, ":", word1Dict.get(word2))
            

    return markovChain


def main():
    #load train and test set files
    testSet = processFileTest()
    #load in train sets to make a Markov Chain
    markovChain = loadTrain()
    #calculate word probabilities
    markovChain = probability(markovChain)
#    markov = MarkovChain(trainSets)

if __name__ == '__main__':
    main()

