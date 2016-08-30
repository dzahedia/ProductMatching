from utilFuncs import *
from model import Model
import os

runFile=os.path.abspath('entrypoint.py')
runDir=os.path.dirname(runFile)
hadoopPath='file://' + runDir

# If your Spark is on a Hadoop culster, uncomment the two following lines and comment the two after
productsFile= hadoopPath + "/data/products.txt"
listingsFile = hadoopPath + "/data/listings.txt"
#productsFile = "data/products.txt"
#listingsFile = "data/listings.txt"

# You can easily change the followings
resultsFile = "result/results.txt"
summaryFile = "result/summary.txt"

if __name__ == "__main__":

    summary = open(summaryFile, 'w')

    model = Model()
    model.train( productsFile)

    summary.write("Succesfully trained the model of products!\n\n")
    summary.write("{0} products were used\n{1} unique key words found.\n\n".format(model.productsCount,model.uniqueWords))
    summary.write("Let's explore the listings.\n")

    model.crunchBatchListings(listingsFile)

    summary.write("On average it took {0:1.3f} milliseconds to crunch each listing based on the trained model.\n\n".format(
            model.avgCrunchTime*1000))

    model.matchBatch(resultsFile)

    summary.write("The results file format; each line:\n {'product_title':'name of the product', listing:[list of the matched]}\n\n")
    summary.write('Some info:\n')
    summary.write("\tGiven the size of the trained matrix, a new listing would take {0:1.3f} milliseconds \
         to run against the model.\n\n".format( model.avgMatchTime* 1000))
    summary.write("\t{0} match found.\n\tfor {1} products, at least, one match was found\n".format(
        model.matchedListCount, model.matchedProdCount))
    summary.close()




