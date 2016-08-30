"""This module includes the implementation of the model as a class."""

import numpy as np
import json
from pyspark import SparkContext
from datetime import datetime
from collections import OrderedDict


from utilFuncs import hiphenReplc, encoding

class Model(object) :

    def train(self, file):
        """This method takes a file and produces a matrix representation of the products in the file"""

        sc = SparkContext()

        initProds = sc.textFile(file)
        self._indexedProds = initProds.zipWithIndex().collectAsMap()
        lines = initProds.map(lambda a: a[1:-1]).map(lambda a : a.replace('"',''))\
            .map(lambda a: a.replace(":", ",")).map(lambda a: a.lower()).cache()
        totlines  =lines.count()
        parsedLines = lines.filter(lambda a: len(a)> 1 )
        self.productsCount = parsedLines.count()
        tokens = parsedLines.map(lambda a: a.split(',')).map(lambda a : a[0:8]).map(hiphenReplc)
        bag = tokens.flatMap(lambda a:a).filter(lambda a: len(a)>1).cache()
        stopwords = ['product','name','manufacturer','model','family']
        noStopWord = bag.filter(lambda a: a not in stopwords)
        self._totalWordsDic = noStopWord.distinct().zipWithIndex().collectAsMap()

        self.trainedMatrix = tokens.map(lambda a: encoding(a,self._totalWordsDic)).collect()

        self.uniqueWords = len(self.trainedMatrix[0])
        sc.stop()

    def saveTrainedMatrix(self):
        "It saves the trained matrix for future use."
        pass

    def crunchSingleListing(self,listing):
        """This method can be implemented for crunching a single listing, for example in an stream app"""
        pass

    def crunchBatchListings(self, file):
        """This method takes a file of listings (in a specified format) and produces matrix rep. of it"""

        sc = SparkContext()

        initListing = sc.textFile(file)
        startTime = datetime.now()
        self._indexedList = initListing.zipWithIndex().collectAsMap()
        listing = initListing.map(lambda a: a[1:-1]).map(lambda a : a.replace('"',''))\
            .map(lambda a: a.replace(":", ",")).map(lambda a:a.replace("(",'')).map(lambda a : a.replace(')',""))\
            .map(lambda a: a.replace('/',' ')).map(lambda a: a.lower()).cache()

        parsedlist = listing.map(lambda a: a.split(',')).map(lambda a : a[1] + a[3])
        tokList = parsedlist.map(lambda a: a.split(" "))
        self.listMatrix = tokList.map(lambda a: encoding(a,self._totalWordsDic)).collect()
        endTime = datetime.now()
        self.totalListings = len(self.listMatrix)
        self.avgCrunchTime = ((endTime-startTime).total_seconds())/self.totalListings
        sc.stop()

    def saveListMatrix(self):
        "It saves the matrix of the listings."
        pass

    def matchSingle(self):
        """This method can be implemented for matching a single listing, for examaple in an stream app"""
        pass

    def matchBatch(self,resultFile):
        """This method runs the listing matrix against the product matrix and writes the result file"""

        outputMat = []
        startTime = datetime.now()
        for i in range(len(self.listMatrix)):
            for j in range(len(self.trainedMatrix)):
                if np.dot(self.trainedMatrix[j],self.trainedMatrix[j]) > 0.90 * (np.dot(self.listMatrix[i],self.trainedMatrix[j])) and \
                                np.dot(self.trainedMatrix[j], self.trainedMatrix[j]) < 1.2 * (np.dot(self.listMatrix[i], self.trainedMatrix[j])):
                    outputMat.append((i,j))
                    break
        endTime = datetime.now()
        totalSec = (endTime - startTime).total_seconds()
        self.avgMatchTime = totalSec/self.totalListings
        self.matchedListCount = len(outputMat)

        invIndList = {k:json.loads(v) for v,k in self._indexedList.items()}
        invIndProd = {k:json.loads(v) for v,k in self._indexedProds.items()}

        outDic = {}
        for k,v in outputMat:
            if v in outDic.keys():
                if k in invIndList.keys():
                    outDic[v]['listings'].append(invIndList[k])
            else:
                outDic[v] = OrderedDict()
                outDic[v]['listings'] = []
                outDic[v]['product_name'] = invIndProd[v]['product_name']
                if k in invIndList.keys():
                    outDic[v]['listings'].append(invIndList[k])

        outJson = list(outDic.values())
        self.matchedProdCount = len(outJson)
        with open(resultFile,'w') as f:
            for i in range(len(outJson)):
                tmp = OrderedDict()
                tmp['product_name'] = outJson[i]['product_name']
                tmp['listings'] = outJson[i]['listings']
                json.dump(tmp, f)
                f.write('\n')


