import rsa
import base64

a, b = rsa.newkeys(16)
c = a.save_pkcs1('PEM').decode("utf-8")
d = c.encode('utf-8')
e = rsa.PublicKey.load_pkcs1(d, 'PEM')
print(a == e)
