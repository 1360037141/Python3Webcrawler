import requests
import base64
import json

code_lists={
    '1':'46,41,',
    '2':'121,38,',
    '3':'182,42,',
    '4':'264,28,',
    '5':'26,119,',
    '6':'122,122,',
    '7':'190,122,',
    '8':'257,108,'
}

session=requests.session()
session.verify=False

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}

url='https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand'
r=session.get(url,headers=headers,verify=False)
r=r.json()['image']
with open('code.jpeg','wb') as p:
    p.write(base64.b64decode(r))

code=input('输入验证码>>> ')
get_code=''
for i in code.split(','):
    get_code+=code_lists[i]

print(get_code)
#验证码校验
data={
    'answer':get_code,
    'login_site':'E',
    'rand':'sjrand'
}

url='https://kyfw.12306.cn/passport/captcha/captcha-check'
r=session.post(url,data=data)
print(r.text)

if '失败' not in r.text:

    login_url = 'https://kyfw.12306.cn/passport/web/login',
    datas={
        'username': '**',
        'password': '**',
        'appid': 'otn',
        'answer': get_code
    }
    r=session.post(login_url,data=datas)
    print(r.text)
    if '错误' or "网络" not in str(r.text):
        url='https://kyfw.12306.cn/passport/web/auth/uamtk'
        data={
            'appid':'otn',
        }
        r=session.post(url,data=data)
        print(r.json())

        apptk=r.json()['newapptk'] or ['apptk']
        url='https://kyfw.12306.cn/otn/uamauthclient'
        data={
            'tk':apptk
        }
        r=session.post(url,data)
        print(r.json())
    else:
        print('登录失败')