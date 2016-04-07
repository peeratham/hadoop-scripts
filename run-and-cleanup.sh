#Hadoop job setup

#Make sure everything is stop before new launch
${HADOOP_HOME}/sbin/stop-dfs.sh
${HADOOP_HOME}/sbin/stop-yarn.sh


#hdfs namenode -format
${HADOOP_HOME}/sbin/start-dfs.sh
${HADOOP_HOME}/sbin/start-yarn.sh

hdfs dfs -rm -R /user

hdfs dfs -mkdir -p /user/tpeera4/input
hdfs dfs -put ${HOME}/input/* /user/tpeera4/input
hdfs dfs -rm /user/tpeera4/input/saved_progress.properties
hdfs dfs -mkdir /user/tpeera4/output
hdfs dfs -mkdir /tmp


hadoop jar ${HOME}/projects/mranalysis/target/mranalysis-1.0-job.jar input output/001

#Copy to Local
hdfs dfs -copyToLocal /user/tpeera4/output/001 ${HOME}/output/

#Archive
d="$(date '+%Y-%m-%d--%H-%M-%S')"
mv ${HOME}/output/001 ${HOME}/output/temp/$d

#Clean up
hdfs dfs -rm -r /user/tpeera4/output/001


#Stop Hadoop
${HADOOP_HOME}/sbin/stop-dfs.sh
${HADOOP_HOME}/sbin/stop-yarn.sh
