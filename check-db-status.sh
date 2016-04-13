echo metadata
mongo analysis --host hslogin1 --eval "db.metadata.count()"
echo reports
mongo analysis --host hslogin1 --eval "db.reports.count()"
echo creators
mongo analysis --host hslogin1 --eval "db.creators.count()"


