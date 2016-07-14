"""Analyze result in MongoDB and output to latex"""

## Imports
from __future__ import division
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import pymongo_spark
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, DoubleType


## Constants
APP_NAME = "Large-Scale Block Smell Analysis"
##OTHER FUNCTIONS/CLASSES

def main(sc, sqlContext, dbname):
   ## get reports 186760
   reports_df = sqlContext.createDataFrame(sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.reports'))
   smells = [cname for cname in reports_df.columns if cname != '_id']
   get_count = lambda record: record['count'] if isinstance(record, dict) else record
   udf_get_count = udf(get_count, IntegerType())
   reports_df = reports_df.select([udf_get_count(reports_df[col]).alias(col) for col in reports_df.columns])
   
   ## get metadata 201851
   project_metadata_df = sqlContext.createDataFrame(sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.metadata'))
   project_metadata_df = project_metadata_df.select('_id', 'creator', 'favoriteCount', 'original', 'remixes', 'views')
      # filter original project
   project_metadata_df = project_metadata_df.filter(project_metadata_df['_id'] == project_metadata_df['original'])
   
   ## get creators 122407
   creators_df = sqlContext.createDataFrame(sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.creators'))
   categories = [u'abstraction', u'Parallelization', u'User Interactivity', u'Synchronization', u'FlowControl', u'Logic', u'DataRepresentation']
   creators_df = creators_df.withColumn('level',sum([creators_df ['mastery'][category] for category in categories]))
   creators_df = creators_df.select(creators_df['_id'].alias('creator'),creators_df['level'])
   
   ## get metrics 179055
   metrics_df = sqlContext.createDataFrame(sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.metrics'))
      # filter trivial projects (zero scripts, 0-1 sprite)?
   metrics_df = metrics_df.filter(metrics_df['scriptCount']>1)
   metrics_df = metrics_df.drop('Mastery Level')
   metrics_df = metrics_df.withColumn('avgScriptLength', metrics_df['Script Length'].getItem("mean"))
   metrics_df = metrics_df.withColumn('sumScriptLength', metrics_df['Script Length'].getItem("sum"))
   metrics_df = metrics_df.drop('Script Length')

   ## join with reports_df then count total
   analysis_df = project_metadata_df.join(reports_df, '_id')
   analysis_df = analysis_df.join(metrics_df, '_id')
   analysis_df = analysis_df.join(creators_df, 'creator')
   
   #################Average Smells Per Script#######################################
   smell_stats_pdf = analysis_df.select(smells).describe().toPandas().transpose()
   smell_stats_pdf.columns = smell_stats_pdf.iloc[0]
   smell_stats_pdf = smell_stats_pdf.reindex(smell_stats_pdf.index.drop('summary'))
   smell_stats_pdf = smell_stats_pdf.drop('count',1)
   smell_stats_pdf = smell_stats_pdf.drop('min',1)
   smell_stats_pdf = smell_stats_pdf.apply(lambda x: pd.to_numeric(x, errors='coerce'))
   write_latex(smell_stats_pdf ,'/home/tpeera4/analysis_output/smell_stats.tex')
   
   #################################################################################
   ################Percent of each smells in the entire population##################
   exists = lambda col: 1 if col > 0 else 0
   udf_exists = udf(exists, IntegerType())
   distinct_smell_df = analysis_df.select(*[udf_exists(column).alias(column) for column in smells])
   with_total_distinct_smells_df = distinct_smell_df.withColumn('Distinct Smell Counts', sum([distinct_smell_df[smell] for smell in smells]))
   row_counts = with_total_distinct_smells_df.count()
   found_smell_sum = with_total_distinct_smells_df.groupby().sum(*smells).toDF(*smells)
   found_smell_sum_pdf = found_smell_sum.toPandas()
   percentage_smell_pdf = found_smell_sum_pdf.applymap(lambda found: found/row_counts*100)
   percentage_smell_pdf = percentage_smell_pdf.transpose()
   percentage_smell_pdf.columns=['freq (%)']
   write_latex(percentage_smell_pdf ,'/home/tpeera4/analysis_output/percent_smell_found.tex')
   ##################################################################################
   #############################Distinct Smells######################################
   ################Summary Smell Stats##################
   combined_stats_pdf = smell_stats_pdf.join(percentage_smell_pdf).round(2)
   combined_stats_pdf.columns.name='Smell'
   write_latex(combined_stats_pdf, '/home/tpeera4/analysis_output/smell_stats.tex')
   #####################################################
   ###################Comparison########################
   current_palette = sns.color_palette("husl", 10)
   metrics = ['scriptCount', 'spriteCount','avgScriptLength', 'sumScriptLength']
   metrics_pdf = analysis_df.groupBy('level').avg(*metrics).toDF('Mastery Level', *metrics).toPandas()
   metrics_pdf = metrics_pdf.set_index('Mastery Level')
   metrics_pdf = metrics_pdf.plot(kind='bar', color=current_palette)
   plt.savefig('/home/tpeera4/analysis_output/mastery-metrics')


   #smell per bloc (block line of code)
   normalize = lambda counts, size: counts/size
   udf_normalize = udf(normalize, DoubleType())
   norm_analysis_df = analysis_df.select(*[udf_normalize(column, analysis_df['sumScriptLength']).alias(column) if column in smells else column for column in analysis_df.columns])

   smells_pdf = norm_analysis_df.groupBy('level').avg(*smells).toDF('Mastery Level',*smells).toPandas()
   smells_pdf = smells_pdf.set_index('Mastery Level')
   smells_pdf.plot(kind='bar', stacked=True, color=current_palette)
   plt.savefig('/home/tpeera4/analysis_output/mastery-smell')

   #population distribution
   level_dist_pdf = analysis_df.groupBy('level').count().toDF('Mastery Level', 'count').toPandas()
   level_dist_pdf = level_dist_pdf.set_index('Mastery Level')
   level_dist_pdf.plot(kind='bar', stacked=True, color=current_palette)
   plt.savefig('/home/tpeera4/analysis_output/mastery-distribution')

   write('Number of projects analyzed', analysis_df.count(), '/home/tpeera4/analysis_output/analysis_summary.txt')
   write('Distinct creators', analysis_df.select('creator').distinct().count(), '/home/tpeera4/analysis_output/analysis_summary.txt')

def write(key,valye, filename):
   with open(filename,'w') as f:
      f.write(key+':'+value)
   
   
def write_latex(pdf, filename):
   with open(filename, 'w') as f:
      f.truncate()
      f.write(pdf.to_latex())


if __name__ == "__main__":
   # Activate pymongo
   pymongo_spark.activate()
   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   sc   = SparkContext(conf=conf)
   # Configure SQLContext
   sqlContext = SQLContext(sc)
   dbname = sys.argv[1]
   # Configure Plotting Libraries
   sns.set()
   plt.switch_backend('agg')
   # Execute Main functionality
   main(sc, sqlContext, dbname)


