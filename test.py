# -*- coding: UTF-8 -*-
import requests as req
import json,sys,time
import random
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用






path=sys.path[0]+r'/Secret.txt'
num1 = 0

def gettoken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':id,
          'client_secret':secret,
          'redirect_uri':'http://localhost:53682/',
          'scope': 'openid offline_access https://graph.microsoft.com/.default'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token

def request(url, headers, index):
    global num1
    n = random.randint(0, 100)
    if n < 50:
        return
    result = req.get(url, headers=headers)
    if result.status_code == 200:
        num1 += 1
        print(str(index) + " success " + str(num1))

def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()

    localtime = time.asctime(time.localtime(time.time()))
    access_token = gettoken(refresh_token)
    headers = {'Authorization': access_token, 'Content-Type': 'application/json'}
    try:
        request(r'https://graph.microsoft.com/v1.0/me', headers, 0)
        request(r'https://graph.microsoft.com/v1.0/me/drive/root', headers, 1)
        request(r'https://graph.microsoft.com/v1.0/me/drive', headers, 2)
        request(r'https://graph.microsoft.com/v1.0/drive/root', headers, 3)
        request(r'https://graph.microsoft.com/v1.0/users', headers, 4)
        request(r'https://graph.microsoft.com/v1.0/me/messages', headers, 5)
        request(r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules', headers, 6)
        request(r'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta', headers, 7)
        request(r'https://graph.microsoft.com/v1.0/me/drive/root/children', headers, 8)
        request(r'https://api.powerbi.com/v1.0/myorg/apps', headers, 9)
        request(r'https://graph.microsoft.com/v1.0/me/mailFolders', headers, 10)
        request(r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories', headers, 11)
    except:
        print("pass")
        pass
for _ in range(5):
    main()
