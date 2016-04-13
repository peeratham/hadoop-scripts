
host=$(hostname)

loginHost="hslogin1"
if [ "$host" != "$loginHost" ]; then
	ssh hslogin1 '/home/tpeera4/projects/scripts/crawler-start.sh'
fi


/home/tpeera4/projects/scripts/run-and-cleanup.sh

/home/tpeera4/projects/scripts/save-analysis-to-db.sh

/home/tpeera4/projects/scripts/check-db-status.sh

