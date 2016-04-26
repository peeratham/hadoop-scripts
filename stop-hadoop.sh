source /home/tpeera4/projects/scripts/configs/hadoop-cluster.conf
ssh ${master} '$HADOOP_HOME/sbin/stop-all.sh'
