"""
Apriori Algorithm for Frequent Itemset Extraction

"""
import sys
import getopt


def generateCandidates(itemsetsK):
    """
    Generate the candidates from large itemsets of previous iteration (L_k).
    Return a dictionary containing candidates formed by joining L_k with L_k.
    """
    C = {}
    lenItemSets = len(itemsetsK)
    for i in range(lenItemSets):
        for j in range(i+1, lenItemSets):
            L1 = itemsetsK[i]
            L2 = itemsetsK[j]
            c1 = {l1 for l1 in L1}
            c2 = {l2 for l2 in L2}
            c1.update(c2)
            fs1 = frozenset(c1)
            C[fs1] = 0
    return C


def pruneCandidates(candidates, sigma):
    """
    Prune candidates which have support lower than sigma.
    Return the candidates having support greater than or equal to sigma and
    their support.
    """
    freqItemSet = {}
    for c in candidates.keys():
        if candidates[c] >= sigma:
            freqItemSet[c] = candidates[c]
    return freqItemSet


def generateFreqItemSets(candidates, transactionList, sigma):
    """
    Generate Large Itemsets (L_k) from candidates, transactionList, and sigma.
    """
    for t in transactionList:
        for c in candidates.keys():
            if c.issubset(t):
                candidates[c] = candidates.get(c, 0) + 1
    return pruneCandidates(candidates, sigma)


def usage(pgm):
    """Print Usage Message"""
    print 'Usage: %s -i <inputfile> -o <outputfile> -s <supportlevel>' % pgm


def strFrozenSet(f):
    """Convert frozenset to a comma separated string"""
    return ", ".join(map(str, f))


def main(argv):
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

    candidates = {}
    transactionList = []
    freqItemSet = {}

    """
    Read all transactions from input file.
    Create candidates of 1-item itemsets (C_1)
    """
    with open(inputfile, "r") as f:
        for transaction in f:
            items = transaction.split()
            intItems = map(int, items)
            trans = frozenset(intItems)
            transactionList.append(trans)
            for intItem in intItems:
                intItemList = [intItem]
                fs = frozenset(intItemList)
                candidates[fs] = candidates.get(fs, 0) + 1

    print "\nCandidates_1 size: %d" % (len(candidates))

    """Create large itemset L_1 from 1-item candidates C_1"""

    freqItemSet = pruneCandidates(candidates, sigma)
    print "FreqItemSet_1 size: %d" % len(freqItemSet.keys())

    k = 2
    with open(outputfile, "w") as opf:
        while (k < len(candidates)):
            """
            Create new candidates (C_k) from L_(k-1)
            Create large itemset L_k from C_k
            """
            newCandidate = generateCandidates(freqItemSet.keys())
            newFreqItemSet = generateFreqItemSets(newCandidate,
                                                  transactionList,
                                                  sigma)
            print "\nCandidates_%d size: %d" % (k+1, len(newCandidate))
            print "FreqItemSet_%d size: %d" % (k+1, len(newFreqItemSet))
            if len(newFreqItemSet) == 0:
                """Stop when |L_k| == 0"""
                print "\nNo new item sets found! Terminating!!!"
                break
            else:
                freqItemSet = newFreqItemSet
            if (k >= 3):
                """Write only frequent item sets with 3 or more items"""
                for fis, v in freqItemSet.items():
                    opf.write("%d, %d, %s\n" % (k, v, strFrozenSet(fis)))
            k = k + 1


if __name__ == "__main__":
    main(sys.argv[:])
