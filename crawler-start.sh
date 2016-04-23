#java -cp ${HOME}/projects/data-manager/target/datamanager-1.0-standalone.jar cs.vt.analysis.datamanager.main.DatasetCrawl \
#-n 10000 -cf /home/tpeera4/projects/scripts/configs/crawler_config.properties -h hslogin1

#java -cp ${HOME}/projects/data-manager/target/datamanager-1.0-standalone.jar cs.vt.analysis.datamanager.main.DatasetCrawl2 -n 10 -db analysis -h hslogin1

java -cp ${HOME}/projects/data-manager/target/datamanager-1.0-standalone.jar -DlogDir="/home/tpeera4/logs/" cs.vt.analysis.datamanager.main.DatasetCrawl2 -n 300 -db analysis -h hslogin1

