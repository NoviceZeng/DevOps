# python-DevOos
> * check_cer：检查域名证书的剩余过期时间，并邮件报警
> * cost-statistics：统计微软云月度账单
> * gitlab_webhooks：利用gitlab的webhook实现向图片服务器的多个项目中进行图片更新，实时触发式更新
> * pull_multi_repo：批量更新多个本地git仓库


# 1. h5-pipeline
## pipeline脚本的注意事项
> * 声明式脚本中通过script使用groovy语法，需要调用定义的环境变量，需要加env，例如本文中，if (env.Branch == 'uat')，测试在scrip中，不能通过echo打印定义的环境变量
> * scp拷贝front目录下的所有文件到远程主机的work目录下： scp -rp /front/* 1.1.1.1:/data/work/；拷贝front文件，则scp -rp /front 1.1.1.1:/data/work/
> * 修改Jenkins的job名字，对应job在workspace下的代码路径也发生改变，所以Jenkinsfile中如有引用路径，需要做出改变
> * Jenkinsfile中涉及的账密、token都可以通过自带的模块，隐式以凭证的方式调用，增加安全性
> * telegram报警，使用Jenkins的插件Telegram Bot，出现偶尔不能收到通知的问题，此处直接通过post的方式发送通知
