"""Calculates the word count of the given file.

the file can be local or if you setup cluster.

It can be hdfs file path"""

## Imports
from __future__ import division
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import pandas as pd
# Activate pymongo
import pymongo_spark


## Constants
APP_NAME = " HelloWorld of Big Data"
##OTHER FUNCTIONS/CLASSES

def main(sc, sqlContext, dbname):
   reports_rdd = sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.reports')
   reports_df = sqlContext.createDataFrame(reports_rdd)
   print reports_df.first()

if __name__ == "__main__":
   # Configure PyMongo
   pymongo_spark.activate()
   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   sc   = SparkContext(conf=conf)
   # Configure SQLContext
   sqlContext = SQLContext(sc)
   dbname = sys.argv[1]
   # Execute Main functionality
   main(sc, sqlContext, dbname)
