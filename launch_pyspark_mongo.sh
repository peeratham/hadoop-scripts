#needs hadoop running
$HADOOP_HOME/sbin/start-all.sh

pyspark --py-files /home/tpeera4/projects/mongo-hadoop/spark/src/main/python/pymongo_spark.py,/home/tpeera4/.local/lib/python2.7/site-packages/pymongo-3.2.2-py2.7-linux-x86_64.egg \
--jars /home/tpeera4/hadoop/share/hadoop/mapreduce/mongo-hadoop-spark-1.5.2.jar \
--driver-class-path /home/tpeera4/hadoop/share/hadoop/mapreduce/mongo-hadoop-spark-1.5.2.jar

#stop hadoop
$HADOOP_HOME/sbin/stop-all.sh
