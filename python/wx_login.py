# coding=utf-8
import time, requests

from flask import json

session = requests.Session()
url = 'https://login.weixin.qq.com/jslogin'
params = {
    'appid': 'wx782c26e4c19acffb',
    'redirect_uri': 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
    'fun': 'new',
    'lang': 'en_US',
    '_': int(time.time()),
    }
r = session.get(url, params = params)
print('Content: %s'%r.text)


import re
regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
# 我们可以看到返回的量是上述的格式，括号内的内容被提取了出来
data = re.search(regx, r.text)
if data and data.group(1) == '200': uuid = data.group(2)
print('uuid: %s'%uuid)


url = 'https://login.weixin.qq.com/qrcode/' + uuid
r = session.get(url, stream = True)
with open('QRCode.jpg', 'wb') as f: f.write(r.content)
# 现在你可以在你存储代码的位置发现一张存下来的图片，用下面的代码打开它
import platform, os, subprocess
if platform.system() == 'Darwin':
    subprocess.call(['open', 'QRCode.jpg'])
elif platform.system() == 'Linux':
    subprocess.call(['xdg-open', 'QRCode.jpg'])
else:
    os.startfile('QRCode.jpg')


import time

while 1:
    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login'
    # 这里演示一下不使用自带的urlencode
    params = 'tip=1&uuid=%s&_=%s'%(uuid, int(time.time()))
    r = session.get(url, params = params)
    regx = r'window.code=(\d+)'
    data = re.search(regx, r.text)
    if not data: continue
    if data.group(1) == '200':
        # 下面一段是为了之后获取登录信息做准备
        uriRegex = r'window.redirect_uri="(\S+)";'
        redirectUri = re.search(uriRegex, r.text).group(1)
        r = session.get(redirectUri, allow_redirects=False)
        redirectUri = redirectUri[:redirectUri.rfind('/')]
        baseRequestText = r.text
        break
    elif data.group(1) == '201':
        print('You have scanned the QRCode')
        time.sleep(1)
    elif data.group(1) == '408':
        raise Exception('QRCode should be renewed')
print('Login successfully')



import xml.dom.minidom
def get_login_info(s):
    baseRequest = {}
    for node in xml.dom.minidom.parseString(s).documentElement.childNodes:
        if node.nodeName == 'skey':
            baseRequest['Skey'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'wxsid':
            baseRequest['Sid'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'wxuin':
            baseRequest['Uin'] = node.childNodes[0].data.encode('utf8')
        elif node.nodeName == 'pass_ticket':
            baseRequest['DeviceID'] = node.childNodes[0].data.encode('utf8')
    return baseRequest
baseRequest = get_login_info(baseRequestText)

url = '%s/webwxinit?r=%s' % (redirectUri, int(time.time()))
data = {
    'BaseRequest': baseRequest,
}
headers = { 'ContentType': 'application/json; charset=UTF-8' }
r = session.post(url, data = json.dumps(data), headers = headers)
dic = json.loads(r.content.decode('utf-8', 'replace'))

print('Log in as %s'%dic['User']['NickName'])
