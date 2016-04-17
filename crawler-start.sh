#source ${HOME}/.profile
java -cp ${HOME}/projects/data-manager/target/datamanager-1.0-standalone.jar cs.vt.analysis.datamanager.main.DatasetCrawl \
-n 100 -cf /home/tpeera4/projects/scripts/configs/crawler_config.properties -h hslogin1
