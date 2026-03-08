# ezy_pzy (BKSEC TTV 2026)
---
## Tổng quan
Trang web cung cấp một trang chủ, trang đăng nhập, đăng ký tài khoản

## Trinh thám

Thử inject các kí tự dặc biệt `'`, `"`,`\` thì server phản hồi lại nguyên xi ==> chứng tỏ k có lỗ hổng SQLi

Tại các trang server có để lại `/utils.js` có chứa credentials

![utils leak](assets/utils%20leak.png)


Khi thử đăng nhập với tên bất kì thì server trả về thông tin key và jwt trong header (leak)

![credentials leak](assets/credentials%20leak.png)

Đưa `X-Debug-Key` đó vào phần sign-key thì nó giải mã được jwt

![jwt decode](assets/jwt%20decode.png)

Do trong body có logged và isAdmin, sửa thành true.

Recon tiếp ở trang login có lộ các endpoints

![login](assets/endpoint%20leak.png)

Sử dụng jwt được sửa thành admin gửi tới các endpoint

![endpoint](assets/get%20api.png)

Gửi `OPTIONS` request tới `/api/dashboard/endpoints` thì cho phép có `post request`

Gửi với post:

![post](assets/post%20api.png)

Recon và server yêu cầu url vè section, url chỉ cho phép **http** và **https** scheme.

Đổi url trong post request thành webhook thì có request tới.

Tuy nhiên tới đây thì em đang bí hướng giải và chưa dùng được dữ kiện `/utils.js`