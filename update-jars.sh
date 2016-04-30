project_path=$HOME/projects

#data-analyzer
cd $project_path/dataset-analyzer
git pull
mvn -q install

#data-manager
cd $project_path/data-manager
git pull
mvn -q install

#mranalysis2
cd $project_path/mranalysis2
git pull
mvn -q install

