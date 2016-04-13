
#read analysis result back to database
java -cp ${HOME}/projects/data-manager/target/datamanager-1.0-standalone.jar \
cs.vt.analysis.datamanager.main.AnalysisResultReader \
-dir ${HOME}/output/result -h "hslogin1"
