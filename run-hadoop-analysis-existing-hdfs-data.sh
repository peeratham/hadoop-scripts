#Hadoop job setup

#make sure not to execute in hslogin1
host=$(hostname)

loginHost="hslogin1"
if [ "$host" == "$loginHost" ]; then
        echo "Cannot execute in" $loginHost
        exit 1
fi

echo "Start execution"



#Archive last analysis result
if [ -d "${HOME}/output/result" ]; then
lastAnalysis=$(cat ${HOME}/output/result/log)
mv ${HOME}/output/result ${HOME}/output/$lastAnalysis
mv ${HOME}/output/$lastAnalysis ${HOME}/output/temp/
fi

echo "DON'T FORGET TO FORMAT NAMENODE ON FIRST USE"

#prevent safemode problem
hdfs dfsadmin -safemode leave

 
hdfs dfs -rm -R /user/tpeera4/output

hdfs dfs -mkdir /user/tpeera4/output
hdfs dfs -mkdir /tmp

hadoop jar ${HOME}/projects/mranalysis2/target/mranalysis2-1.0-job.jar input output/result

#Copy to Local
hdfs dfs -copyToLocal /user/tpeera4/output/result ${HOME}/output/

#Archive
d="$(date '+%Y-%m-%d--%H-%M-%S')"
echo $d >> ${HOME}/output/result/log

#Clean up
hdfs dfs -rm -r /user/tpeera4/output/result


