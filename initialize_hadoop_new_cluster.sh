
source /home/tpeera4/projects/scripts/configs/hadoop-cluster.conf
ssh ${master} 'hdfs namenode -format'
ssh ${master} '/home/tpeera4/hadoop/sbin/stop-dfs.sh'
ssh ${master} '/home/tpeera4/hadoop/sbin/stop-yarn.sh'
ssh ${master} '/home/tpeera4/hadoop/sbin/start-dfs.sh'
ssh ${master} '/home/tpeera4/hadoop/sbin/start-yarn.sh'
