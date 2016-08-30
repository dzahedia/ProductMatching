from utils import *
from model import Model

resultsFile = "result/results.txt"
summaryFile = "result/summary.txt"
productsFile = "data/products.txt"
listingsFile = "data/listings.txt"

if __name__ == "__main__":

    summary = open(summaryFile, 'w')

    model = Model()
    model.train( productsFile)

    summary.write("Succesfully trained the model of products!\n\n")
    summary.write("{0} products were used\n{1} unique key words found.\n".format(model.productsCount,model.uniqueWords))
    summary.write("Let's explore the listings.\n")

    model.crunchBatchListings(listingsFile)

    summary.write("On average it took {0:1.3f} milliseconds to crunch each listing based on the trained model.\n".format(
            model.avgCrunchTime*1000))

    model.matchBatch(resultsFile)

    summary.write("The results file format; each line:\n {'product_title':'name of the product', listing:[list of the matched]}\n")
    summary.write('Some info:\n')
    summary.write("Given the size of the trained matrix, a new listing would take {0:1.3f} milliseconds \
         to run against the model.\n".format( model.avgMatchTime* 1000))
    summary.write("{0} match found.\n/tfor {1} products, at least, one match was found\n".format(
        model.matchedListCount, model.matchedProdCount))
    summary.close()




