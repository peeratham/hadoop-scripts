$HADOOP_HOME/sbin/start-all.sh
hdfs dfsadmin -safemode leave

hdfs dfs -rm -R /user/tpeera4/input
hdfs dfs -rm -R /user/tpeera4/output

hdfs dfs -mkdir -p /user/tpeera4/input
hdfs dfs -put ${HOME}/input/* /user/tpeera4/input
hdfs dfs -rm /user/tpeera4/input/saved_progress.properties
hdfs dfs -mkdir /user/tpeera4/output
hdfs dfs -mkdir /tmp

$HADOOP_HOME/sbin/stop-all.sh
