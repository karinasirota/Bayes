# Name: Rosalie Chan (rmc982) and Karina Sirota (kss118)
# Date: May 22, 2016
# Description:
# All group members were present and contributing during all work on this project
#

import math, os, pickle, re, random

class Bayes_Classifier:
    
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
        if (os.path.exists("negative2.txt") and os.path.exists("positive2.txt")):
            self.posDict = self.load("positive2.txt")
            self.negDict = self.load("negative2.txt")
        else:
            self.posDict = {}
            self.negDict = {}
            self.train()
    
    def train(self, inputData = 0):
        """Trains the Naive Bayes Sentiment Classifier."""
        
        IFileList = []
        for fFileObj in os.walk("movies_reviews/"):
            IFileList = fFileObj[2]
            for fileName in IFileList:
                star = fileName[7]
                #print star
                review = self.loadFile("movies_reviews/"+fileName)
                token = self.tokenize(review)
                if (star == '5'):
                    for word in token:
                        posEntry = {word: 1}
                        if word in self.posDict:
                            self.posDict[word] += 1
                        else:
                            self.posDict.update(posEntry)
                else:
                    for word in token:
                        negEntry = {word: 1}
                        if word in self.negDict:
                            self.negDict[word] += 1
                        else:
                            self.negDict.update(negEntry)
                
                test = [i+' '+j for i,j in zip(token[::2], token[1::2])]
                if (star == '5'):
                    for word in test:
                        posEntry = {word: 1}
                        if word in self.posDict:
                            self.posDict[word] += 1
                        else:
                            self.posDict.update(posEntry)
                else:
                    for word in test:
                        negEntry = {word: 1}
                        if word in self.negDict:
                            self.negDict[word] += 1
                        else:
                            self.negDict.update(negEntry)
        self.save(self.negDict, "negative2.txt")
        self.save(self.posDict, "positive2.txt")
        # return posDict, negDict 
            
    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
        posProb = float(0)
        priorPos = float(11129)/float(13864)
        negProb = float(0)
        priorNeg = float(2735)/float(13864)
        total = float(13864)
        token = self.tokenize(sText)
        # test = [i+' '+j for i,j in zip(token[::2], token[1::2])]
        test = [i+' '+j for i,j in zip(*[token[i:] for i in range(2)])] 
        if (len(token)%2 == 1):
            test.append(token[len(token) - 1])

        for word in token:
            if word in self.posDict:
                if (posProb == float(0)):
                    posProb = math.log(priorPos)
                # print "negProb", negProb
                # print "posProb", posProb
                posProb += math.log(float((self.posDict[word]+1) / total))
                # print "newposProb", negProb
            else:
                posProb += math.log(float(1)/total)
            if word in self.negDict:
                if (negProb == float(0)):
                    negProb = math.log(priorNeg)
                # print "negProb", negProb
                # print "posProb", posProb
                negProb += math.log(float((self.negDict[word]+1) / total))
                # print "newnegProb", negProb
            else:
                negProb += math.log(float(1)/total)
        
        for word in test:
            if word in self.posDict:
                if (posProb == float(0)):
                    posProb = math.log(priorPos)
                # print "negProb", negProb
                # print "posProb", posProb
                posProb += math.log(float((self.posDict[word]+1) / total))
                # print "newposProb", negProb
            else:
                posProb += math.log(float(1)/total)
            if word in self.negDict:
                if (negProb == float(0)):
                    negProb = math.log(priorNeg)
                # print "negProb", negProb
                # print "posProb", posProb
                negProb += math.log(float((self.negDict[word]+1) / total))
                # print "newnegProb", negProb
            else:
                negProb += math.log(float(1)/total)
        if (posProb > negProb):
            return 'positive'
        elif (negProb > posProb):
            return 'negative'
        else:
            return 'neutral'

    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""
        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt
   
    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()
   
    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText): 
        """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))
               
        if sToken != "":
            lTokens.append(sToken)

        return lTokens

    def validate(self):
        trainingData = []
        testingData = []
        positiveData = []
        negativeData = []
        totalRecall = 0
        totalPrecision = 0
        totalFMeasure = 0 

        for fFileObj in os.walk("movies_reviews/"):
            trainingData = fFileObj[2]
            break
        
        negativeData = trainingData[:2735]
        positiveData = trainingData[2635:]
            
        for i in range(100):
            print "Current Iteration:", i 
            truePositive = 0
            trueNegative = 0
            falsePositive = 0
            falseNegative = 0
            totalPositive = 0
            totalNegative = 0

            #make random
            random.shuffle(positiveData)
            random.shuffle(negativeData)
            #choose 10% testing data
            positiveTestData = positiveData[0:(len(positiveData)/10)]
            negativeTestData = negativeData[0:(len(negativeData)/10)]
            testingData = positiveTestData + negativeTestData
            #remove testing from training
            trainingData = [x for x in trainingData if x not in testingData]
            print "Training data"

            self.train(inputData = trainingData)

            for fileName in testingData:
                
                review = self.loadFile("movies_reviews/"+fileName)
                result = self.classify(review)

                if result == 'positive':
                    if (fileName[7] == '5'):
                        truePositive += 1
                    else:
                        falsePositive += 1
                    totalPositive +=1
                if result == 'negative':
                    if (fileName[7] == '1'):
                        trueNegative += 1
                    else:
                        falseNegative += 1 
                    totalNegative += 1


            #recall= fraction of correctly classification
            recall = float(truePositive) / float(truePositive + falseNegative)
            totalRecall = totalRecall + recall
            print "totalrecall", float(totalRecall / 10)
            
            #Precision: faction of assigned to I to total about I 
            precision = float(truePositive) / float(truePositive + falsePositive)
            totalPrecision = totalPrecision + precision
            print "Precision", float(totalPrecision / 10)

            #2PR/(P+R)
            fmeasure = 2 * (float(precision) * float(recall)) / float(precision + recall)
            totalFMeasure = totalFMeasure + fmeasure
            print "fmeasure",  float(totalFMeasure / 10) 


