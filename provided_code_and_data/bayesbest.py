# Name: Rosalie Chan (rmc982) and Karina Sirota (kss118)
# Date: May 22, 2016
# Description:
# All group members were present and contributing during all work on this project
#

import math, os, pickle, re

posDict = {}
negDict = {}
class Bayes_Classifier:
    
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
        self.train()
    
    def train(self):
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
                        if word in posDict:
                            posDict[word] += 1
                        else:
                            posDict.update(posEntry)
                else:
                    for word in token:
                        negEntry = {word: 1}
                        if word in negDict:
                            negDict[word] += 1
                        else:
                            negDict.update(negEntry)
                test = [i+' '+j for i,j in zip(token[::2], token[1::2])]
                if (star == '5'):
                    for word in test:
                        posEntry = {word: 1}
                        if word in posDict:
                            posDict[word] += 1
                        else:
                            posDict.update(posEntry)
                else:
                    for word in test:
                        negEntry = {word: 1}
                        if word in negDict:
                            negDict[word] += 1
                        else:
                            negDict.update(negEntry)
        self.save(negDict, "negative.txt")
        self.save(posDict, "positive.txt")
        return posDict, negDict 
            
    
    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
        posProb = float(0)
        negProb = float(0)
        total = float(13864)
        token = self.tokenize(sText)
        test = [i+' '+j for i,j in zip(token[::2], token[1::2])]
        if (len(token)%2 == 1):
           test.append(token[len(token) - 1])

        for word in test:
            if word in posDict:
                if (posProb == float(0)):
                    posProb = float(1)
                # print "negProb", negProb
                # print "posProb", posProb
                posProb *= float(posDict[word] / total)
                # print "newposProb", negProb
            if word in negDict:
                if (negProb == float(0)):
                    negProb = float(1)
                # print "negProb", negProb
                # print "posProb", posProb
                negProb *= float(negDict[word] / total)
                # print "newnegProb", negProb
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
