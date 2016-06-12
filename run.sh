#!/bin/bash
SPARK_SUBMIT=$SPARK_HOME/bin/spark-submit

$SPARK_SUBMIT --master=local[20] sparkFreqItems.py "$@"
