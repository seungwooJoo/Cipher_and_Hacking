from Crypto.Cipher import AES
from Crypto.Hash import SHA256 as SHA

class myAES():
    def __init__(self, keytext, ivtext): #클래스를 호출 할 때에, 최초로 자동으로 호출되는 함수로, 초기화 할 때 사용된다.
        hash = SHA.new()  #SHA256객체를 만들고 hash에 할당한다. 
        hash.update(keytext.encode('utf-8'))  #keytext를 인자로 하여 SHA256해시갱신을 한다.
        key = hash.digest() # 해시 값을 추출하여 변수 key에 할당합니다.and
        self.key = key[:16] 
        
        hash.update(ivtext.encode('utf-8')) #암호키 생성과 마찬가지로 초기화벡터를 생성하기 위해서도 SHA256 해시를 활용한다. 초기화 벡터를 위한 해시 갱신
        iv = hash.digest() # digest()함수로 해시 값을 얻은 후 변수 iv에 담는다.
        self.iv = iv[:16] #AES는 암호화를 수행하는 블록크기가 128비트이므로 초기화벡터는 16바이트 크기로 한다. 
        
        
    def makeEnabled(self, plaintext):
        fillersize=0
        textsize = len(plaintext)
        if textsize % 16 != 0 :
            fillersize = 16 - textsize%16

        filler = '0'*fillersize
        header = '%d' %(fillersize)
        gap = 16 - len(header)
        header += '#'*gap

        return header+plaintext+filler

    def enc(self, plaintext):
        plaintext = self.makeEnabled(plaintext)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        encmsg = aes.encrypt(plaintext)
        return encmsg
    
    def dec(self, ciphertext):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        decmsg = aes.decrypt(ciphertext)
        
        header = decmsg[:16].decode() #복호화된 정보 decmsg의 처음 16바이트를 유니코드로 변환 
        fillersize = int(header.split('#')[0]) #split('#')으로 header를 '#'을 구분자로 분리한다. 분리된 값중 첫번째를 정수로 변환한다
        if fillersize !=0:
            decmsg = decmsg[16:-fillersize]
        else:
            decmsg = decmsg[16:]
        return decmsg
    
def main():
    keytext = 'korea'
    ivtext = '190719'
    msg = 'jooseungwoo'

    myCipher = myAES(keytext, ivtext)
    ciphered = myCipher.enc(msg)
    deciphered = myCipher.dec(ciphered)
    print('ORIGINAL: \t%s' %msg)
    print('CIPHERED: \t%s' %ciphered)
    print('DECIPHERED: \t%s' %deciphered)
   
if __name__ == '__main__':
    main()
