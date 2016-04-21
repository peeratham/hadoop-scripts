source /home/tpeera4/projects/scripts/configs/hadoop-cluster.conf

ssh ${master} '/home/tpeera4/projects/scripts/run-hadoop-analysis-new-data'

/home/tpeera4/projects/scripts/save-analysis-to-db.sh

/home/tpeera4/projects/scripts/check-db-status.sh

/home/tpeera4/projects/scripts/run-pyspark-analysis-script.sh

/home/tpeera4/projects/scripts/save-to-dropbox.sh
