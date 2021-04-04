# 1. prometheus安装、tg报警及相关注意事项

## 1.1 注意事项
1. prometheus、alertmanager默认使用utc时区，比cst慢了8小时，docker运行时使用 *-v /etc/localtime:/etc/localtime* 或者 *ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime* 
   的方式只能改变容器的时间，prom和alertmanager web界面中显示的时间是代码中定义的，只有修改代码中对应的时区才能修改报警时web界面显示的时间
2. 服务器系统的时区不一致可能导致alertmanager接收不到报警；另外docker镜像中全部统一默认UTC时区，不影响报警，tg显示的时区时间独立于容器中的时区时间；
3. aws node节点不放行9100端口，Prometheus会一直不报警，因为
## 1.2 Prometheus安装
```
docker run -d -p 9090:9090 \
-v /data/prometheus/:/prometheus/ \
--restart=always \
--name=prometheus \ 
pro/prometheus
```
配置文件见prometheus.yml、first_rules.yml

## 1.3 Alertmanager安装
```
docker run -d \
  -p 9093:9093 \
  --name alertmanager \
  --restart=always \
  -v /data/alertmanager:/etc/alertmanager \
  prom/alertmanager
 ```
 配置文件见alertmanager.yml
 
 ## 1.4 alertmanager-bot报警安装
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
