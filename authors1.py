#authors.py
#
#Marina Schwadron

import sys
import StemmingUtil
import math
import string
from copy import deepcopy

punctuation=['!','``','\'\'','#','$','%','&','\'','(',')','*','+',',','-','--','.','/',':',';',\
'<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~','“','”','"']

class Node():
    def __init__(self, author, totalWords, countUnique):
        self.author = author
        self.totalWords = totalWords
        self.wordDict = {}
        self.probDict = {}
        self.countUnique = countUnique
        self.curseCount = 0
        self.curseScore = 0
    def countWords(self, wordList, curseWords):
        curseCount = self.curseCount
        curseScore = self.curseScore
        wordDict = self.wordDict
        probDict = self.probDict
        #build a dictionary of word counts
        for word in wordList:
            if len(word)!=0 and word not in wordDict.keys():
                wordDict[word] = 1
            elif len(word)!=0 and word in wordDict.keys():
                wordDict[word] += 1
            if word in curseWords:
                curseCount += 1
        #build a dictionary of word probabilities
        for word in wordDict.keys():
            if wordDict.get(word):
                p = (wordDict.get(word) + 1)/(self.totalWords + self.countUnique)
                probDict[word] = p
        self.curseScore = curseCount/self.totalWords
##        print(self.author)
##        print(self.curseScore)

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

def NaiveBayes(trainSets, allUnique):
    #create a node for each author, which will contain a dictionary of words and their counts
    authorNodes = {} #Dict of author nodes
    curseWords = []
    curseFile = open("CurseWords.txt", encoding = "utf-8", mode = "r")
    for word in curseFile:
        word = word.replace('\n', '')
        curseWords.append(word)
    for book in trainSets.keys():
        N = Node(trainSets.get(book)[0], len(trainSets.get(book)[1:]), len(allUnique))
        N.countWords(trainSets.get(book)[1:], curseWords)
        #create dictionary entry with {author: Node}
        authorNodes[trainSets.get(book)[0]] = N
    return authorNodes
        
def Prediction(testSet, authorNodes, trainSets):
    curseWords = []
    curseFile = open("CurseWords.txt", encoding = "utf-8", mode = "r")
    for word in curseFile:
        word = word.replace('\n', '')
        curseWords.append(word)
    bestSum = -100000000
    bestAuthor = ""
    bestAuthors = []
    bestCurse = 1
    bestCurAuth = ""
    bestCAs = []
    sumA = 0
    count = 0
    for passage in testSet:
        count += 1
        for book in trainSets.keys():
            passCurse = 0
            passCurScore = 0
            totalW = 0
            author = trainSets.get(book)[0]
            aNode = authorNodes.get(author)
            for w in passage:
                totalW += 1
                #print(w)
                if len(w)!=0:
                    if w in aNode.probDict.keys():
                        sumA += math.log(aNode.probDict.get(w))
                    else: 
                        sumA += math.log(1/(aNode.countUnique + aNode.totalWords))
                    if w in curseWords:
                        passCurse += 1
            passCurseScore = passCurse/totalW
            print(author, sumA)
            if sumA > bestSum:
                bestSum = sumA
                bestAuthor = author
            sumA = 0
            curseComp = abs(passCurseScore - aNode.curseScore)
            if curseComp < bestCurse:
                bestCurAuth = author
                bestCurse = curseComp
        bestAuthors.append(bestAuthor)
        bestCAs.append(bestCurAuth)
    print(bestAuthors)
    print(bestCAs)
    return bestAuthors
    
def writeFile(matrix):
    #create output file
    file = "results_authors.csv"
    f = open(file, "w+")
    #print matrix
    labels = ",".join(map(str, matrix[0]))
    f.write(labels + ","+"\n")
    for i in range(1, len(matrix)):
        string = ",".join(map(str, matrix[i]))
        f.write(string+"\n")
    #close the file
    f.close()


def main():
    #load train and test set files
    testSet = processFileTest()
    trainSets, allUnique = loadTrain()
    authorNodes = NaiveBayes(trainSets, allUnique)
    #go through each author in the test set and get their predictions
    #create a list of all author labels
    allAuthors = []
    #create a confusion matrix
    matrix = []
    #first line in matrix is a list of authors
    for a in trainSets.keys():
        allAuthors.insert(0, trainSets.get(a)[0])
    allAuthors.insert(0, "Authors")
    matrix.append(allAuthors)
    for testAuthor in allAuthors[1:]:
        #1st item in line is the actual label
        mLine = [testAuthor]
        for a in allAuthors[1:]:
            mLine.append(0)
        #create a list of predictions for each passage for this author
 #       print(testSet.get(testAuthor+" "),testAuthor)
        prediction = Prediction(testSet.get(testAuthor + " "), authorNodes, trainSets)
        for p in prediction:
            mLine[allAuthors.index(p)] += 1
        #add line to matrix
        matrix.append(mLine)

    writeFile(matrix)

if __name__ == '__main__':
    main()
