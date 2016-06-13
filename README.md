Mining Frequent Item Sets
=========================

FreqItemSets
--------------
This repo contains all the source files, test files, and output files for the
problem of extracting frequent item sets with 3 or more items and having support
greater than or equal to a user supplied paramater, sigma.

---
# Apriori Algorithm

The first implementation that I tried uses Apriori Algorithm. This algorithm works 
by initially creating single item item sets as Candidates, C_1. The items which have 
support greater than or equal to sigma are retained to form Large Item Set, L_1.

Succeeding C_k and L_k are formed as follows.

* C_k is formed by joining L_(k-1) and L_(k-1)
* L_k is formed by pruning item sets from C_k which have support less than sigma

This process stops when |L_k| is empty.

## Running the program

`python freqItems -i <inputfile> -o <outputfile> -s <sigma>`

All arguments are mandatory. As expected, this works well for smaller test cases
such as `test.dat` which has 2 frequent item sets when sigma = 2.

Profiling with `-m cProfile` shows that most of the time is spent in generateFreqItemSets().
A significant portion is spent in the issubset() check.

It takes a long, long, long time to run for larger test cases as there are a lot of 
candidates that are created and tested.

---
# Using Pandas

The second implementation that I tried used brute force with Pandas. Again this takes a
long, long time to run. Hence, abandoned this approach. 

There were lot of issues in reading ragged files using read_csv. Have tried 2 workaround -
* Read file line by line and create new DataFrames and concatenate with previous. Inefficient, so discarded.
* Hardcoded the maximum number of items in a transaction.

This code was experimental and as such has hardcoded input.

`python pandasFreqItems.py`

---

# FPGrowth

The third approach that I tried uses FP Growth algorithm that avoids inefficiencies of Apriori by not 
generating all candidates. The algorithm can be found at [here](https://www.cs.sfu.ca/~jpei/publications/sigmod00.pdf).

I used the Spark MLLib implementation of the same. Set the $SPARK_HOME to your Spark installation path.


`run.sh -i <inputfile> -o <outputfile> -s <sigma>`


 


