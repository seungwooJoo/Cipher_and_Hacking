from Crypto.Hash import SHA256 as SHA
SIZE = 1024 * 256

def getFileHash(filename):
    hash = SHA.new()
    h = open(filename, 'rb')
    content = h.read(SIZE)
    while content:
        hash.update(content)
        hashval = hash.digest()
        content = h.read(SIZE)
    h.close()
    return hashval

def hashCheck(file1, file2):
    hashval1 = getFileHash(file1)
    hashval2 = getFileHash(file2)
    if hashval1 == hashval2:
        print('Two Files are Same')
    else : 
        print('Two Files are Different')
        
def main():
    file1 = 'text.txt'
    file2 = 'text.txt.enc.dec'
    hashCheck(file1, file2)
    
if __name__ == '__main__':
    main()