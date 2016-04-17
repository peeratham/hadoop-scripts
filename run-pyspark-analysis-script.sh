#$HADOOP_HOME/sbin/start-all.sh

host=$(hostname)
loginHost="hslogin1"
if [ "$host" != "$loginHost" ]; then
echo "Error: Client needs to hslogin not cluster nodes"
exit 1
fi

spark-submit \
--master yarn \
--deploy-mode client \
--py-files="/home/tpeera4/projects/mongo-hadoop/spark/src/main/python/pymongo_spark.py" \
--driver-class-path="/home/tpeera4/hadoop/share/hadoop/mapreduce/mongo-hadoop-spark-1.5.2.jar" \
/home/tpeera4/projects/spark-mongo-analysis/result-analysis.py
