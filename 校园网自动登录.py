import os
import sys
import time
import requests
import socket
import uuid
from ping3 import ping
from win10toast import ToastNotifier
temp_=os.path.realpath(sys.argv[0])
#认证服务器不同地址也不同

def ping_():
    num=ping("223.5.5.5",)
    if num is None:
        return "no"
    else:
        return "ok"
# 如果有网就直接结束程序
if ping_()=="ok":
    ToastNotifier().show_toast(title="该设备已登录",
                               msg="校园网状态 OK。。。",
                               icon_path=os.path.dirname(temp_)+"\ico\Check.ico",
                               duration=30,
                               threaded=False)
    sys.exit()
# 账号
userId=""
# 密码要加密后的，不能是加密前的
password=""
EPORTAL_USER_GROUP=""#多久入学填几几年
# 电信1，移动2，联通3，内网4
sc="2"
#dz是你们学校认证服务器的地址，不同学校地址不一样
dz="192.168.8.1"
# default 是校园内网
# ctc 是中国电信
# cmcc 是中国移动
# unicom 是中国联通
EPORTAL_COOKIE_SERVER=""
#cookie 下面填需要你自己抓包，标头的cookie的最后有类似：
# JSESSIONID="093DD499BB09E5C421286D66CF430000"的，把JSESSIONID=""里面的内容复制粘贴就行
JSESSIONID=""





if sc=="1":
    EPORTAL_COOKIE_SERVER = "ctc"
elif sc=="2":
    EPORTAL_COOKIE_SERVER = "cmcc"
elif sc == "3":
    EPORTAL_COOKIE_SERVER = "unicom"
elif sc=="4":
    EPORTAL_COOKIE_SERVER = "default"
#     以太网和wifi的识别
# 自动获取电脑ip(弃用)
    # 函数 gethostname() 返回当前正在执行 Python 的系统主机名
# ip = socket.gethostbyname(socket.gethostname())

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(('223.5.5.5',80))
    ip=s.getsockname()[0]
finally:
    s.close()
print(ip)
# 获取电脑mac

mac = uuid.UUID(  int=uuid.getnode() ).hex[-12:]

# 请求头

headers={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "760",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": f"EPORTAL_COOKIE_DOMAIN=false; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_USERNAME={userId}; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_COOKIE_NEWV=true; EPORTAL_COOKIE_PASSWORD={password}; EPORTAL_USER_GROUP={EPORTAL_USER_GROUP}; EPORTAL_COOKIE_SERVER=; EPORTAL_COOKIE_SERVER_NAME=; JSESSIONID={JSESSIONID}",
    "Host": f"{dz}",
    "Origin": f"http://{dz}",
    "Referer": f"http://{dz}/eportal/index.jsp?wlanuserip={ip}&wlanacname=GZY-CORE-N18K-V&ssid=&nasip=192.168.200.254&snmpagentip=&mac={mac}&t=wireless-v2-plain&url=http://www.msftconnecttest.com/redirect&apmac=&nasid=GZY-CORE-N18K-V&vid=2605&port=145&nasportid=AggregatePort%20106.26050000:2605-0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
}
# 表单数据
data={
    "userId": userId,
    "password": password,
    "service": EPORTAL_COOKIE_SERVER,
    "queryString": f"wlanuserip%3D{ip}%26wlanacname%3DGZY-CORE-N18K-V%26ssid%3D%26nasip%3D192.168.200.254%26snmpagentip%3D%26mac%3D{mac}%26t%3Dwireless-v2-plain%26url%3Dhttp%3A%2F%2Fwww.msftconnecttest.com%2Fredirect%26apmac%3D%26nasid%3DGZY-CORE-N18K-V%26vid%3D2605%26port%3D145%26nasportid%3DAggregatePort%2520106.26050000%3A2605-0",
    "operatorPwd": "",
    "operatorUserId": "",
    "validcode": "",
    "passwordEncrypt": "true"
}

session=requests.session()

url=f"http://{dz}/eportal/InterFace.do?method=login"
while(True):

    if sc=="1":
        #     电信
        print("正在登陆请稍后。。。。")
        session.post(url=url, headers=headers, data=data)
        session.post(url=f"http://{dz}/eportal/success.jsp")
        ping_()
        time.sleep(2)
        if ping_() == "ok":
            ToastNotifier().show_toast(title="该设备已登录",
                                       msg="校园网状态 OK。。。",
                                       icon_path=os.path.dirname(temp_) + "\ico\Check.ico",
                                       duration=30,
                                       threaded=False)
            sys.exit()
    elif sc=="2":
        #     移动
        print("正在登陆请稍后。。。。")
        session.post(url=url,headers=headers, data=data)
        session.post(url=f"http://{dz}/eportal/success.jsp")
        time.sleep(2)
        ping_()
        if ping_() == "ok":
            ToastNotifier().show_toast(title="该设备已登录",
                                       msg="校园网状态 OK。。。",
                                       icon_path=os.path.dirname(temp_) + "\ico\Check.ico",
                                       duration=30,
                                       threaded=False)
            sys.exit()
    elif sc=="3":
        #     联通
        print("正在登陆请稍后。。。。")
        session.post(url=url, headers=headers, data=data)
        session.post(url=f"http://{dz}/eportal/success.jsp")
        ping_()
        time.sleep(2)
        if ping_() == "ok":
            ToastNotifier().show_toast(title="该设备已登录",
                                       msg="校园网状态 OK。。。",
                                       icon_path=os.path.dirname(temp_) + "\ico\Check.ico",
                                       duration=30,
                                       threaded=False)
            sys.exit()
    elif sc=="4":
        #     校园内网
        print("正在登陆请稍后。。。。")
        session.post(url=url, headers=headers, data=data)
        session.post(url=f"http://{dz}/eportal/success.jsp")
        ping_()
        time.sleep(2)
        if ping_() == "ok":
            ToastNotifier().show_toast(title="该设备已登录",
                                       msg="校园网状态 OK。。。",
                                       icon_path=os.path.dirname(temp_) + "\ico\Check.ico",
                                       duration=30,
                                       threaded=False)
            sys.exit()
    else:
        print("请重新输入！")
        continue


