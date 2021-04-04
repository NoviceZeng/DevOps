# prometheus安装、tg报警及相关注意事项

## 1. 注意事项
1. prometheus、alertmanager默认使用utc时区，比cst慢了8小时，docker运行时使用 *-v /etc/localtime:/etc/localtime* 或者 _ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime_ 
   的方式只能改变容器的时间，prom和alertmanager web界面中显示的时间是代码中定义的，只有修改代码中对应的时区才能修改报警时web界面显示的时间
2. 服务器系统的时区不一致可能导致alertmanager接收不到报警；另外docker镜像中全部统一默认UTC时区，不影响报警，tg显示的时区时间独立于容器中的时区时间；
3. aws node节点不放行9100端口，Prometheus会一直不报警，因为prom拉取报metrics *http://172.31.27.236:9100/metrics*  时没有给任何超时响应，只是卡在那离，不返回结果，所以不报警。
   其中，prometheus.yml的 *scrape_timeout* 超时时间设置没有起到作用

## 2. tg bot创建相关
1. 请参考(官方文档)[https://core.telegram.org/bots] 中第三步通过BotFather创建bot并获取token，通过向 *@userinfobot* 发送任何消息获取chat id;
2. **如果tg接收不到报警，一定要想到是否在对应群组里面运行/start，开始报警**，如下图所示
   ![image](https://user-images.githubusercontent.com/33800153/113503653-dc963880-9565-11eb-8fa8-356be3f95ace.png)

## 3. Prometheus安装
```
docker run -d -p 9090:9090 \
-v /data/prometheus/:/prometheus/ \
--restart=always \
--name=prometheus \ 
pro/prometheus
```
配置文件见prometheus.yml、first_rules.yml

## 4. Alertmanager安装
```
docker run -d \
  -p 9093:9093 \
  --name alertmanager \
  --restart=always \
  -v /data/alertmanager:/etc/alertmanager \
  prom/alertmanager
 ```
 配置文件见alertmanager.yml
 
 ## 5. alertmanager-bot报警安装
 ```
 docker run  -d \
        -e 'ALERTMANAGER_URL=http://172.31.23.2:9093' \
        -e 'BOLT_PATH=/data/bot.db' \
    -p 8080:8080 \
        -e 'STORE=bolt' \
        -e 'TELEGRAM_ADMIN=111111111' \
        -e 'TELEGRAM_TOKEN=1171888888:AAHJl9N_m07_isiXQrLiNV9E0aaaaaaGSY' \
        -v '/data/bot_alert:/data' \
        --name alertmanager-bot \
        metalmatze/alertmanager-bot:0.4.3
```
## 6. node_exporter安装
1. 官方(GitHub)[https://github.com/prometheus/node_exporter/releases/tag/v1.1.2)下载对应版本；
2. 解压并命名到/opt/node_exporter中；
3. 运行命令 _nohup ./node_exporter  >> /data/logs/monitor/node_exporter.log 2>&1 &_
