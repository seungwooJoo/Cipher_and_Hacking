from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256 as SHA

class myARC4():
    def __init__(self, keytext):
        self.key = keytext
        
    def enc(self, plaintext):
        arc4 = ARC4.new(self.key) #self.key를 키로 하여 ARC4 객체를 생성하고 이를 변수 arc4에 할당
        encmsg = arc4.encrypt(plaintext)
        return encmsg
    
    def dec(self, ciphertext):
        arc4 = ARC4.new(self.key)
        decmsg = arc4.decrypt(ciphertext)
        return decmsg

    
def main():
    keytext = 'miki'
    msg='jooseungwoo'
    
    myCipher = myARC4(keytext)
    ciphered = myCipher.enc(msg)
    deciphered = myCipher.dec(ciphered)
    print('ORIGINAL: \t%s' %msg)
    print('CIPHERED: \t%s' %ciphered)
    print('DECIPHERED: \t%s' %deciphered)
    
    
if __name__ == '__main__':
    main()