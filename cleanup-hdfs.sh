hdfs dfsadmin -safemode leave

hdfs dfs -rm -R /user/tpeera4/input
hdfs dfs -rm -R /user/tpeera4/output
hdfs dfs -rm -R /tmp/logs/tpeera4/logs/

hdfs dfs -mkdir -p /user/tpeera4/input
hdfs dfs -put ${HOME}/input/* /user/tpeera4/input
hdfs dfs -rm /user/tpeera4/input/saved_progress.properties
hdfs dfs -mkdir /user/tpeera4/output
hdfs dfs -mkdir /tmp

