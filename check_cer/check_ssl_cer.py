# coding: utf-8
# 查询域名证书到期情况
import time, re, threading, subprocess, yagmail
from datetime import datetime
from io import StringIO
def check_ssl(domain):
    f = StringIO()
    comm = f"curl -Ivs https://{domain} --connect-timeout 10"
    result = subprocess.getstatusoutput(comm)
    f.write(result[1])
    m = re.search('start date: (.*?)\n.*?expire date: (.*?)\n.*?common name: (.*?)\n.*?issuer: CN=(.*?)\n', f.getvalue(), re.S)
    start_date = m.group(1)
    expire_date = m.group(2)
    common_name = m.group(3)
    issuer = m.group(4)

    # time 字符串转时间数组
    start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
    start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)

    # datetime 字符串转时间数组
    expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
    expire_date_st = datetime.strftime(expire_date,"%Y-%m-%d %H:%M:%S")

    # 剩余天数
    remaining = (expire_date-datetime.now()).days
    #print ('域名:', domain)
    #print ('通用名:', common_name)
    #print ('开始时间:', start_date_st)
    #print ('到期时间:', expire_date_st)
    #print (f'剩余时间: {remaining}天')
    #print ('颁发机构:', issuer)
    #print ('*'*30)

    results = {}
    results['domain_name'] = domain.strip()
    results['remain'] = remaining
    return results

# 发送邮件
def send_mail(**expire_list):
    user = 'thomson@e-veb.com'
    password = '123456789012'
    # gmail
    host = 'smtp.gmail.com'
    to =['server@e-veb.com','thomson@e-veb.com','zero@e-veb.com','axel@e-veb.com','bob@e-veb.com','alexander@e-veb.com','hamilton@e-veb.com']
    subject = 'ssl证书过期预警'
    d = ''
    d += '''\
  <tr>
    <td align="center">''' + expire_list['domain_name'] + '''</td>
    <td align="center">''' + str(expire_list['remain']) + '''</td>
  </tr>
'''
    html = '''\
<table width="70%" border="1" bordercolor="black" cellspacing="0" cellpadding="0">
  <tr>
    <td width="140" align="center" ><strong>域名</strong></td>
    <td width="110" align="center" ><strong>剩余天数</strong></td>
  </tr>
'''+ d +'''</table>'''
  # 去除邮件中多余换行
    html = html.replace("\n", "")
    yag = yagmail.SMTP(user = user, password = password, host = host)
    yag.send(to = to, subject = subject, contents = html)

if __name__ == "__main__":
    expire_domain_list = []
    with open('domain_lists.txt') as domains:
        for domain in domains:
            expire_domain_list = check_ssl(domain)
            if expire_domain_list['remain'] <= 50:
                send_mail(**expire_domain_list)
