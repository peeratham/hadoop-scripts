source /home/tpeera4/projects/scripts/configs/analysis-variables.conf

echo metadata
mongo $dbname --host hslogin1 --eval "db.metadata.count()"
echo reports
mongo $dbname --host hslogin1 --eval "db.reports.count()"
echo metrics
mongo $dbname --host hslogin1 --eval "db.metrics.count()"
echo creators
mongo $dbname --host hslogin1 --eval "db.creators.count()"
echo sources
mongo $dbname --host hslogin1 --eval "db.sources.count()"

