echo "===update configuration==="

echo ":::update master node info:::"


hadoop_config_dir="$HOME/hadoop-configuration-kwang"

master_node_before="hs008"
master_node_after="hs043"


sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/mapred-site.xml
sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/core-site.xml
sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/hdfs-site.xml
sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/yarn-site.xml
sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/kms-site.xml
sed -Ei "s|${master_node_before}|${master_node_after}|" ${hadoop_config_dir}/hadoop-metrics.properties


#Slave node

echo ":::update slave node info:::"






slave_nodes=(
"hs046"
"hs027"
)

#clear old info
truncate -s 0 ${hadoop_config_dir}/slaves

for node in "${slave_nodes[@]}"
do
        printf "%s\n" $node >> ${hadoop_config_dir}/slaves
done



echo "---------Changes Summary----------"
grep -r "hs[0-9][0-9][0-9]" $HOME/hadoop-configuration-kwang
