from Crypto.PublicKey import RSA
def readPEM():
    h = open('mykey.pem', 'r')
    key = RSA.importKey(h.read())
    h.close()
    return key

def rsa_enc(msg):
    private_key = readPEM()
    public_key = private_key.publickey() #private_key로부터 공개키를 얻고,
    encdata = public_key.encrypt(msg,32) # 이 공개키로 메시지를 암호화합니다.
    return encdata

def rsa_dec(msg):
    private_key = readPEM()
    decdata = private_key.decrypt(msg)
    return decdata

if __name__ == '__main__':
    msg = 'JooSeungwoo'
    ciphered = rsa_enc(msg.encode('utf-8'))
    print(ciphered)
    deciphered = rsa_dec(ciphered)
    print(deciphered)
