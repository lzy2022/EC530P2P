import rsa
import base64

public_key_addr = './SeverKey_Public.pem'
private_key_addr = './SeverKey_Private.pem'
PAYLOAD_SIZE = 2048

print('Generating New Key Sets...')
public_k, private_k = rsa.newkeys(PAYLOAD_SIZE)
pub_f = open(public_key_addr, 'wb')
pub_f.write(public_k.save_pkcs1('PEM'))
pub_f.close()
pri_f = open(private_key_addr, 'wb')
pri_f.write(private_k.save_pkcs1('PEM'))
pri_f.close()
