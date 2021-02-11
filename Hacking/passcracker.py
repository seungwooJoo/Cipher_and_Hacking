import crypt

def findpass(passhash, dictfile):
    salt = passhash[3:5]
    with open(dictfile,'r') as dfile:
        for word in dfile.readlines():
            word = word.strip('\n')
            cryptwd = crypt.crypt(word,salt)
            if cryptwd == passhash[3:]:
                return word
    return ''

def main():
    dictfile = 'dictionary.txt'
    with open('passwords.txt', 'r') as passFile:
        for line in passFile.readlines():
            data = line.split(':')
            user = data[0].strip()
            passwd = data[1].strip()
            word = findpass(passwd, dictfile)
            if word:
                print('FOUND Password : ID [%s] Password [%s]' %(user,word))
            else : 
                print('Password Not Found!')

                
if __name__ == '__main__':
    main()
    
# 이 코드는 패스워드 해시 유형이 $1$1 즉, MD5로 해시값을 계산했을 떄 유효한 코드입니다. SHA256, SHA512로 적용한 패스워드 해시유형을
# 적용하려면 crypt.crypt()를 SHA256, SHA512를 지원하는 것으로 바꾸면 됩니다. 