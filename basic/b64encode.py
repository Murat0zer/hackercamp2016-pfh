import base64

flag = "Hackercamp 2016 biz buradayiz oley"
for i in range(10):
    flag = base64.b64encode(flag)

print flag
