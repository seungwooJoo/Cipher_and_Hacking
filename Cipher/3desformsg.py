from Crypto.Cipher import DES3
from Crypto.Hash import SHA256 as SHA

class myDES():
    def __init__(self, keytext, ivtext): #클래스를 호출 할 때에, 최초로 자동으로 호출되는 함수로, 초기화 할 때 사용된다.
        hash = SHA.new()  #SHA256객체를 만들고 hash에 할당한다. 
        hash.update(keytext.encode('utf-8'))  #keytext를 인자로 하여 SHA256해시갱신을 한다.
        key = hash.digest() # 해시 값을 추출하여 변수 key에 할당합니다.and
        self.key = key[:24] #Pycrypto에서 제공하는 3DES 키 크기는 16byte or 24byte. 이게 아니면 오류가 나기 떄문에 16바이트 또는 24바이트 만큼 슬라이싱 하여 3DES키로 사용한다. 
        
        hash.update(ivtext.encode('utf-8')) #암호키 생성과 마찬가지로 초기화벡터를 생성하기 위해서도 SHA256 해시를 활용한다. 초기화 벡터를 위한 해시 갱신
        iv = hash.digest() # digest()함수로 해시 값을 얻은 후 변수 iv에 담는다.
        self.iv = iv[:8] #iv의 처음 8바이트를 초기화 벡터값으로 할당한다.and 
        
    def enc(self, plaintext):  #인자로 입력된 plaintext에 담긴 문자열을 3DES로 암호화한다. 
        des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv) #3DES객체 생성. 인자는 순서대로 '암호키','운영모드', '초기회 벡터'다.and
        encmsg = des3.encrypt(plaintext)
        return encmsg
        
    def dec(self, ciphertext):
        des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv) 
        decmsg = des3.decrypt(ciphertext)
        return decmsg
    
def main():
    keytext = 'korea'
    ivtext = '190719'
    msg = 'jooseung'

    myCipher = myDES(keytext, ivtext)
    ciphered = myCipher.enc(msg)
    deciphered = myCipher.dec(ciphered)
    print('ORIGINAL: \t%s' %msg)
    print('CIPHERED: \t%s' %ciphered)
    print('DECIPHERED: \t%s' %deciphered)
    
if __name__ == '__main__':
    main()

#암호화 하려는 메시지 길이는 8바이트의 배수여야 한다. 8바이트 배수가 아닌 문자열이더라도 오륲없이 암호화하고 복호화가 가능하도록 수정한 코드는 3desformsg_modified.py에서..