from __future__ import division
from pyspark import SparkContext, SparkConf
from pyspark import SQLContext as sqlCtx
import pymongo_spark

import sys
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, MapType
pymongo_spark.activate()

from pyspark.sql import SQLContext

#creating SparkContext
sc = SparkContext(appName="ResultAnalysis")
sqlContext = SQLContext(sc)

# Using Mongo as data source
reports_rdd = sc.mongoRDD('mongodb://hslogin1:27017/analysis.reports')
reports_df = sqlContext.createDataFrame(reports_rdd)

# Smell Frequency
cnames = reports_df.columns 
metadata = ['Mastery Level', '_id', 'scriptCount', 'spriteCount']
smells = [name for name in reports_df.columns if name not in metadata]
smell_reports_cnames = smells+['_id']
smell_reports_df = reports_df.select(smell_reports_cnames)


def get_count(record):
     if isinstance(record, dict):
          return record['count']
     else:
          return record

udf_get_count = udf(get_count,IntegerType())
smell_freq_reports = reports_df.select([udf_get_count (reports_df[smell]).alias(smell) for smell in smell_reports_cnames])

average_smells = smell_freq_reports.groupby().avg(*smells).toDF(*smells)     #count all instances in each project
smell_instance_counts = smell_freq_reports.groupby().sum(*smells).toDF(*smells)

#total smells for each instance
with_total_smells = smell_freq_reports.withColumn('Total Smells', sum([smell_freq_reports[smell] for smell in smells]))

#todo distinct smells
exists = lambda col: 1 if col > 0 else 0
udf_exists = udf(exists, IntegerType())
distinct_smell_df = smell_freq_reports.select(*[udf_exists(column).alias(column) if column in smells else column for column in smell_reports_cnames])


with_total_distinct_smells_df = distinct_smell_df.withColumn('Distinct Smell Counts', sum([distinct_smell_df[smell] for smell in smells]))

#compute percent of each type of smell
row_counts = with_total_distinct_smells_df.count()
found_smell_sum = with_total_distinct_smells_df.groupby().sum(*smells).toDF(*smells)
found_smell_sum_pdf = found_smell_sum.toPandas()

percentage_smell_pdf = found_smell_sum_pdf.applymap(lambda found: found/row_counts*100)

percentage_smell_pdf = percentage_smell_pdf.transpose()
percentage_smell_pdf.columns=['freq (%)']

print(percentage_smell_pdf)

#write to analysis_output
fo = open('/home/tpeera4/analysis_output/frequency.tex', 'w')
fo.truncate()
fo.write(percentage_smell_pdf.to_latex())
fo.close()


#shutdown Spark
sc.stop()
