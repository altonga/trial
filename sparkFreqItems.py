"""
Frequent Item Set Extraction using Spark MLLib FPGrowth Implementation

"""
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.fpm import FPGrowth
import sys
import getopt

APP_NAME = "Frequent Item Sets"


def printItemSet(items):
    """Return a comma separated string containing all elements in items"""
    return ", ".join(map(str, items))


def usage(pgm):
    """Return usage message"""
    print 'Usage: %s -i <inputfile> -o <outputfile> -s <supportlevel>' % pgm


def main(sc, argv):
    inputfile = ''
    outputfile = ''
    sigma = 0

    """
    Parse command line option

    * inputfile: csv file containing the transaction data (delimiter is ' ')
    * outputfile: csv file containing frequent item sets of size 3 or more
                  with support greater than sigma
    * sigma: minimum support required (should be positive integer)
    """
    try:
        opts, args = getopt.getopt(argv[1:],
                                   "hi:o:s:", ["ifile=", "ofile=", "sigma="])
    except getopt.GetoptError:
        usage(argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage(arg[0])
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--sigma"):
            sigma = int(arg)

    print 'Input file is ', inputfile
    print 'Output file is ', outputfile
    print 'Support level is ', str(sigma)
    if inputfile == '' or outputfile == '' or sigma <= 0:
        usage(argv[0])
        sys.exit(2)

    data = sc.textFile(inputfile)
    transactions = data.map(lambda line: line.strip().split(' '))
    """Compute minSupport from sigma"""
    minSupport = float((float(sigma))/transactions.count())
    print "MinSupport = " + str(minSupport)
    model = FPGrowth.train(transactions, minSupport, numPartitions=10)
    result = model.freqItemsets().collect()
    with open(outputfile, "w") as opf:
        for items, freq in result:
            if len(items) >= 3:
                """Write only frequent item sets with 3 or more items"""
                opf.write("%d, %d, %s\n" %
                          (len(items), freq, printItemSet(items)))


if __name__ == "__main__":
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc = SparkContext(conf=conf)
    main(sc, sys.argv[:])
