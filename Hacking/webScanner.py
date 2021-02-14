from urllib.request import urlopen, Request, URLError, quote
from queue import Queue
from threading import Thread


user_agent = 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'

def webScanner(q, targethost, exts):       #exts는 추가적으로 스캔하고자 하는 파일 확장자를 담은 리스트다.
    while not q.empty():                 #인자로 받은 큐 객체에 데이터가 없어질 때 까지 동작한다. 
        scanlist = []                    #접속할 URI를 담기위한 리스트 자료. 
        toscan = q.get()                    #큐에서 데이터를 얻음. 
        if '.' in toscan: #FILE            
            scanlist.append('%s' %toscan)
            for ext in exts:
                scanlist.append('%s%s' %(toscan,ext))
        else: #DIR       큐에서 전달받은 데이터에 '.'이 없을 경우 디렉터리 이름이므로 '/'를 주가한 후 scanlist에 추가한다.,
            scanlist.append('%s/' %toscan)
            
        for toscan in scanlist:            #scanlist에 있는 모든 URI에 대해 접속할 수 있는 URL을 구성한 후 접속을 시도. 성공하면 응답코드와 접속한 URL을 화면에 출력
            url = '%s/%s' %(targethost, quote(toscan))
            try:
                req=Request(url)
                req.add_header('User-Agent', user_agent)
                res = urlopen(req)
                if len(res.read()):
                    print('[%d]: %s' %(res.code, url))
                res.close()
            except URLError as e:
                pass

def main():
    targethost = 'http://125.209.222.141' #www.naver.com
    wordlist='./SVNDigger/all.txt'
    exts = ['-', '~1', '.back', '.bak', '.old', '.orig', '_backup']
    q=Queue()
    
    with open(wordlist, 'rt') as f:
        words = f.readlines()       # readlines()는 결과를 리스트 자료로 리턴하므로 words는 리스트 자료가 된다
    
    for word in words:
        word = word.rstrip()        #오른쪽 공백 제거
        q.put(word)
        
    print('+++[%s] SCANNING START...' %targethost)
    for i in range(50):                #webScanner를 실행하기 위한 50개의 스레드 구동
        t = Thread(target = webScanner, args = (q, targethost, exts))
        t.start()
        
        
if __name__ == '__main__':
    main()
    
    