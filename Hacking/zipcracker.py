import zipfile                        #zipfile모듈은 ZIP파일을 생성하고 읽고 기록하고, 압축풀기와 같은 zip파일 관련 다양한 메소드를 제공
from threading import Thread            #ZIP파일 패스워드 크래킹은 스레드를 구동하여 구현할 것이므로 threading 모듈의  Thread 모듈을 import 한다

def crackzip(zfile, passwd):        #인자로 zipfile객체와 사전에서 선택한 패스워드 passwd를 인자로 받아 해당 zip파일의 압축 해제를 시도.
    try:
        zfile.extractcall(pwd=passwd)     #passwd를 패스워드로 하여 zfile의 모든 내용에 대해 압축해제를 시도한다. 
        print('ZIP file extracted successfully! PASS = [%s]' %passwd.decode())
        return True
    except:
        pass
    return False

def main():
    dictfile = 'dictionary.txt'
    zipfilename = 'locked.zip'
    zfile = zipfile.Zipfile(zipfilename, 'r')
    pfile = open(dictfile, 'r')
    
    for line in pfile.readlines():
        passwd = line.strip('\n')
        t = Thread(target = crackzip, args = (zfile, passwd.encode('utf-8')))        #crackzip함수를 독립된 스레드로 호출한다.
        #스레드는 하나의 프로세스 안에 있는 또 다른 작은 프로세스이다. 스레드로 호출하는 이유는 crackzip()이 연산하는 동안 for 구문을 계속 수행하여 보다 효율적으로 패스워드 크래킹을 하기 위함.
        t.start()
        
if __name__ == '__main__':
    main()