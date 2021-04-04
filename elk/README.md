# 1. 概述
## 1.1 版本概述
filebeat 6.8、logstash 6.8、kafka 2.11-2.3.0(其中2.11为scala版本，2.3.0为kafka版本)、es 7.9(使用aws自带)；  
测试用logstash 7以上版本，向es7.3和7.9中写入报错。

## 1.2 kafka常用命令
启动zoopkeeper  
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > /data/logs/zk.log 2>&1 &  
启动kafka  
nohup bin/kafka-server-start.sh config/server.properties > /data/logs/kafka.log 2>&1 &

创建topic，同一个topic在不同partitions的数据是不重复的；
replication的数量不能大于Broker的数量，follower和leader绝对是在不同的机器，同一机器对同一个分区也只可能存放一个副本。  
kafka-topics.sh --create --zookeeper 172.31.0.23:2181,172.31.0.24:2181,172.31.0.25:2181 --topic nginx-access --partitions 2  --replication-factor 2

查看日志是否从filebeat传输过来，该topic不用手动创建，日志传输后会从filebeat中定义output.kafka.topic中获取  
bin/kafka-console-consumer.sh --bootstrap-server 172.31.0.23:9092 --topic nginx-access --from-beginning

## 1.3 配置
filebeat收集nginx日志见：ELK/nginx-log-map/filbeat-6.8.yaml
logstash接受kafka的日志配置见：ELK/nginx-log-map/logstash-6.8.conf

### 1.3.1 logstash注意事项  
> * output中输出到es的index需要以logstash-命名开始，如index => "**logstash-** XXX"；如果不这样命令，kibana地图查询ip，Aggregation中没有Geohash选项报错；
> * [@metadata][kafka][timestamp]不能在filter中remove，删除后，output index中就不能用时间定义日志名称；
> * [@metadata][kafka][timestamp]删除后，如果json格式的message中有同名@timestamp，并展开到root中后，会覆盖原来的@timestap；

### 1.3.2 logstash常用命令
安装插件命令  
bin/logstash-plugin install logstash-filter-geoip       #查看插件list

测试插件配置，用如下命令，并将消费者输出到屏幕(见配置)  
bin/logstash -f config/logstash.conf --config.reload.automatic





