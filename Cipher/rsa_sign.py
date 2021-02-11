from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256 as SHA

def readPEM():
    h = open('mykey.pem', 'r')
    key = RSA.importKey(h.read())
    h.close()
    return key

#사용자의 개인키로 서명하는 측
def rsa_sign(msg):
    private_key = readPEM()
    public_key = private_key.publickey()
    hash = SHA.new(msg).digest()  #digest()로 해시값을 추출 , msg의 SHA256해시를 구하고,
    signature = private_key.sign(hash, '') # hash값에 개인키로 서명을 하였다. 
    return public_key, signature

#사용자의 공개키로 서명을 확인하는 측
def rsa_verify(msg, public_key, signature):   #서명을 확인하는 쪽에서는 '확인해야 할 msg와 공개키를 알고 있다'고 가정해야 하며,
                                              #개인키로 서명한 정보는 네트워크를 통해 이미 전달받았다고 생각해야 한다. 
    hash = SHA.new(msg).digest()        #확인하고자 하는 msg의 SHA256 해시를 구하고ㅡ,  verify()함수,. 
    if public_key.verify(hash, signature):
        print('VERIFIED')
    else:
        print('DENIED')
        
if __name__ == '__main__':
    msg = 'My name is Jooseungwoo'
    public_key, signature = rsa_sign(msg.encode('utf-8'))
    rsa_verify(msg.encode('utf-8'), public_key, signature)