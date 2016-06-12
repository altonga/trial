"""
Brute Force to Extract Frequent Itemsets using Pandas
"""
import pandas as pd
from itertools import combinations

"""
The commented code is an alternative way for reading in the data.
This is because read_csv does not handle variable length records.
It determines the number of columns based on first row.
So if there is a row with more number of fields, it causes pandas
to bomb out.
An inefficient workaround is reading line by line and creating new
dataframes and concatenating to existing one.
Another approach (which I took here) is to specify the engine as python
and the number of items.
I have lot of hard coded stuff in this file as it is not really a good
approach but was an experimental effort.

To avoid problems due to trailing ' ', i preprocessed input file to remove
trailing spaces as below:
sed 's/[ \t]*$//' retail_25k.dat > retail_25k_c.dat

"""
# import numpy as np
# from StringIO import StringIO


transactions = pd.read_csv('retail_25k_c.dat', header=None, delimiter=' ',
                           engine='python', names=range(74))
transactions = transactions.where((pd.notnull(transactions)), None)


# df = pd.DataFrame()
# with open("retail_25k.dat", 'r') as f:
#     k = 0
#     for line in f:
#  #       print "%d: " % (k)
#         k += 1
#         text = StringIO(line.strip())
#         l = pd.read_csv(text, delimiter=' ', header=None)
# #        print l
#         df = pd.concat([df, l])
# #    print df

transactionItemMatrix = \
    pd.get_dummies(transactions.unstack().dropna()).groupby(level=1).sum()
transactionCnt, itemCnt = transactionItemMatrix.shape
print transactionCnt
print itemCnt

largeItemsets = []
for items in range(1, itemCnt+1):
    for itemset in combinations(transactionItemMatrix, items):
        itemsetSupport = transactionItemMatrix[list(itemset)].all(axis=1).sum()
        s = [str(int(x)) for x in itemset]
        if (len(s) >= 3):
            largeItemsets.append([",".join(s), itemsetSupport])
freqItemset = pd.DataFrame(largeItemsets, columns=["Itemset", "Support"])
results = freqItemset[freqItemset.Support >= 2]
print results
