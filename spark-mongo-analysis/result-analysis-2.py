from __future__ import division
from pyspark import SparkContext
from pyspark.sql import SQLContext
import pandas as pd
# Activate pymongo
import pymongo_spark
pymongo_spark.activate()

#def write_latex(pdf,filename):
#   fo = open(filename, 'w')
#   fo.truncate()
#   fo.write(pdf.to_latex())
#   fo.close()

def write_latex(pdf, filename):
   with open(filename, 'w') as f:
      f.truncate()
      f.write(pdf.to_latex())

# get SparkContext & sqlContext
sc = SparkContext(appName="ResultAnalysis")
sqlContext = SQLContext(sc)

dbname = 'analysis'
# get reports
reports_rdd = sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.reports')
reports_df = sqlContext.createDataFrame(reports_rdd)
# get metadata
project_metadata_rdd = sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.metadata')
project_metadata_df = sqlContext.createDataFrame(project_metadata_rdd)
# get creators
creators_rdd = sc.mongoRDD('mongodb://hslogin1:27017/'+dbname+'.creators')
creators_df = sqlContext.createDataFrame(creators_rdd)


# set columns
# exclude 'Mastery Level' in metadata
metadata = ['_id', 'scriptCount', 'spriteCount', 'Mastery Level']
smells = [name for name in reports_df.columns if name not in metadata]


#################Average Smells Per Script########################################
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, DoubleType

get_count = lambda record: record['count'] if isinstance(record, dict) else record
udf_get_count = udf(get_count, IntegerType())
smell_cnames =  smells + ['_id', 'scriptCount', 'spriteCount']
smell_freq_df = reports_df.select([udf_get_count(reports_df[col]).alias(col) for col in smell_cnames])
# filter trivial projects (zero scripts, 0-1 sprite)?
smell_freq_df = smell_freq_df.filter(smell_freq_df['scriptCount'] > 0)

# normalized (divided by scriptCounts to account for various project size)
normalized_by_script = lambda smell, script: smell/script
udf_norm_smell = udf(normalized_by_script, DoubleType())
norm_smell_freq_df = smell_freq_df.select([udf_norm_smell(smell_freq_df[smell], smell_freq_df['scriptCount']).alias(smell) for smell in smells])
average_smells_per_script = norm_smell_freq_df.groupby().avg(*smells).toDF(*smells)
average_smells_per_script_pdf = average_smells_per_script.toPandas()
average_smells_per_script_pdf = average_smells_per_script_pdf.transpose()
average_smells_per_script_pdf.columns=['Avg. Smells per Script']
write_latex(average_smells_per_script_pdf ,'/home/tpeera4/analysis_output/smell_per_script.tex')
#################################################################################
################Percent of Projects Found to contain each smell##################
exists = lambda col: 1 if col > 0 else 0
udf_exists = udf(exists, IntegerType())
distinct_smell_df = smell_freq_df.select(*[udf_exists(column).alias(column) for column in smells])
with_total_distinct_smells_df = distinct_smell_df.withColumn('Distinct Smell Counts', sum([distinct_smell_df[smell] for smell in smells]))
row_counts = with_total_distinct_smells_df.count()
found_smell_sum = with_total_distinct_smells_df.groupby().sum(*smells).toDF(*smells)
found_smell_sum_pdf = found_smell_sum.toPandas()
percentage_smell_pdf = found_smell_sum_pdf.applymap(lambda found: found/row_counts*100)
percentage_smell_pdf = percentage_smell_pdf.transpose()
percentage_smell_pdf.columns=['freq (%)']
write_latex(percentage_smell_pdf ,'/home/tpeera4/analysis_output/percent_smell_found.tex')
##################################################################################
################Summary Smell Stats##################
combined_stats = average_smells_per_script_pdf.join(percentage_smell_pdf).round(2)
write_latex(combined_stats, '/home/tpeera4/analysis_output/smell_stats.tex')
#####################################################


