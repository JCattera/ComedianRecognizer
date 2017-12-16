import nltk
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer

punctuation=['``','\'\'','#','$','%','&','\'','(',')','*','+',',','-','--','/',':',';', '\ ','<','=','>','@',
             '[','\\',']','^','_','`','{','|','}','~','“','”','"',"\n"]

def loadTrain():
    Texts = {}
    Texts["Iglesias"] = open("Gabriel_Iglesias.txt", encoding = "utf-8", mode = 'r')
    Texts["Izzard"]=open("Eddie_Izzard1.txt", encoding = "utf-8", mode = 'r')
    Texts["Silverman"]=open("Sarah_Silverman.txt", encoding = "utf-8", mode = 'r')
    Texts["Noah"]=open("Trevor_Noah.txt", encoding = "utf-8", mode = 'r')
    Texts["Mulaney"]=open("John_Mulaney.txt", encoding = "utf-8", mode = 'r')
    Texts["Buress"] = open("Hannibal_Buress.txt", encoding = "utf-8", mode = 'r')
    Texts["Burnham"]=open("Bo_Burnham.txt", encoding = "utf-8", mode = 'r')
    Texts["Ansari"]=open("Aziz_Ansari.txt", encoding = "utf-8", mode = 'r')
    Texts["Sykes"]=open("Wanda_Sykes.txt", encoding = "utf-8", mode = 'r')

    return Texts

def findScores(Texts):
    endpunct= ['!',"?","."]
    Scores = {}
    for Text in Texts.keys():
        train = []
        sentence = ""
        for line in Texts.get(Text):
            for p in punctuation:
                line= line.replace(p,'')
            listLine = line.split(' ')
            #print(listLine)
            for w in listLine:
                sentence = sentence + " " + w
                for p in endpunct:
                    if p in w:
                        train.append(sentence)
                        sentence = ""
        
        sid = SentimentIntensityAnalyzer()
        totalScore = 0
        sentences = 0
        for sentence in train:
            sentences += 1
            ss = sid.polarity_scores(sentence)
            totalScore += ss.get('compound')
        Scores[Text] = totalScore/sentences
    return Scores


def Test(TrainScores):
    print(TrainScores)
    endpunct= ["!","?","."]
    Predictions = {}
    TestScores = {}
    TestFile = open("TestSet_Passages.txt", encoding="utf-8", mode="r")
    testDict = {}
    for line in TestFile:
        test = []
        sentence = ""
        if "#" in line:
            #read line after "###" as the comic
            comic = TestFile.readline()
            comic = comic.replace('\n', '')
            continue
        else:
            for p in punctuation:
                line= line.replace(p,'')
            listLine = line.split(' ')
            for w in listLine:
                sentence = sentence + " " + w
                for p in endpunct:
                    if p in w:
                        test.append(sentence)
                        sentence = ""
            if comic not in testDict.keys():
                testDict[comic] =[test]
            else:
                testDict.get(comic).append(test)

    for comic in testDict.keys():
        TestScores[comic] = []
        tests = testDict.get(comic)
        Predictions[comic] = []
        #print(tests)
        for passage in tests:
            sid = SentimentIntensityAnalyzer()
            totalScore = 0
            sentences = 0
            for sentence in passage:
                sentences += 1
                ss = sid.polarity_scores(sentence)
                totalScore += ss.get('compound')
            TestScore = totalScore/sentences
            TestScores.get(comic).append(TestScore)

    return TestScores
    
            

def main():
      
    # Step 1 – Training data
    Texts = loadTrain()
    TrainScores = findScores(Texts)
    TestScores = Test(TrainScores)
    print("Train Scores")
    for i in TrainScores.keys():
        print(i, ":", TrainScores.get(i))

    print()

    print("Test Scores")
    for i in TestScores.keys():
        print(i, ":", TestScores.get(i))



    

if __name__ == '__main__':
    main()
