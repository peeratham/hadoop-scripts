source /home/tpeera4/projects/scripts/configs/analysis-variables.conf

java -cp $HOME/projects/data-manager/target/datamanager-1.0-standalone.jar \
cs.vt.analysis.datamanager.main.ExportData \
-e /home/tpeera4/mongodb/bin/mongoexport \
-h hslogin1 \
-d $dbname \
-c sources \
-o $HOME/input \
-n 10000

