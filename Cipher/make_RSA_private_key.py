from Crypto.PublicKey import RSA

def createPEM():
    private_key = RSA.generate(1024)
    f = open('mykey.pem', 'wb+')
    f.write(private_key.exportKey('PEM'))
    f.close()

if __name__ == '__main__':
    createPEM()
