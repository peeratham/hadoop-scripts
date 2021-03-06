source /home/tpeera4/projects/scripts/configs/hadoop-cluster.conf
source /home/tpeera4/projects/scripts/configs/analysis-variables.conf

host=$(hostname)

loginHost="hslogin1"
if [ "$host" != "$loginHost" ]; then
	echo "Script can only execute at the client hslogin1 not cluster nodes"
	exit 1
fi

#/home/tpeera4/projects/scripts/cleanup-input.sh

#/home/tpeera4/projects/scripts/export-input-sources.sh

ssh ${master} '/home/tpeera4/projects/scripts/run-hadoop-analysis-new-data.sh'

/home/tpeera4/projects/scripts/save-analysis-to-db.sh

/home/tpeera4/projects/scripts/check-db-status.sh

/home/tpeera4/projects/scripts/run-pyspark-analysis-script.sh $dbname

/home/tpeera4/projects/scripts/save-to-dropbox.sh

