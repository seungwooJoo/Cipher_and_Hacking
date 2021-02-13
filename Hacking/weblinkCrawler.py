from urllib.request import urlopen, Request
import re
import sys

user_agent = 'Mozilla/5.0\(compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
href_links = []

def getLinks(doc, home, parent):                #인자로 전달된 HTML 페이지 내용인 doc에 존재하는 모든 'href'태그를 찾아 링크 정보를 얻는 함수.
    #인자로 주어진 parent 는 doc에 해당하는 URI의 상위 경로 정보이다. 
    
    global href_links
    href_pattern = [r'href=\S+"', r'href=\S+ ', r'href=\S+\'']        
    #href="링크정보"
    #href=링크정보
    #href='링크정보'
    
    tmp_urls = []
    
    for n in range(len(href_pattern)):
        tmp_urls += re.findall(href_pattern[n],doc, re.I)    #re.I는 대소문자 구분하지 말고 패턴 매치를 수행하라는 의미다. 
        
    for url in tmp_urls:
        url = url.strip()
        url = url.replace('\'','"')                #href='링크정보' -> href="링크정보"
        if url[-1] is ' ' or url.find('"') is -1:     #href=링크정보
            url = url.split('=')[1]
        else:                                            ##href="링크정보"
            url = url.split('"')[1]
        
        if len(url) is 0:
            continue
            
        if url.find('http://') is -1:    #링크정보가 'http://'로 시작하지 않으면 내부 경로 형태로 되어 있는 경우다.
            if url[0] == '/':            #'/'로 시작하는 경우는 웹사이트의 홈주소를 추가하면 제대로 된 링크정보가 된다. 
                url = home + url
            elif url[:2] == './':        #'./'로 시작하거나 그 외의 경우는 'http://parent/url'이 올바른 링크정보가 될 것이다 
                url = 'http://' + parent + url[1:]
            else:
                url = 'http://' + parent + '/' + url
        
        if url in href_links:
            continue
        
        if '.html' not in url:            #url이 HTML페이지가 아니면 href_links 리스트에 추가하고 다음 for문 처리를 위해 넘어감
            href_links.append(url)
            continue
            
        runCrawler(home,url)                #HTML페이지이면 getLinks() 함수를 호출한 runCrawler() 함수를 호출한다.
        
def readHtml(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', user_agent)
        h = urlopen(req)
        doc = h.read()            #read()는 바이트 문자열을 리턴한다. 
        h.close()
    except Exception as e:
        print('ERROR : %s' %url)
        print(e)
        return None
    return doc.decode()     다       #바이트 문자열을 유니코드로 변환하여 리턴한다. 

def runCrawler(home, url):
    global href_links
    href_links.append(url)
    
    print('GETTING ALL LINKS IN [%s]' %url)
    try:
        doc = readHtml(url)
        if doc is None:
            return
    
        tmp = url.split('/')
        parent = '/'.join(tmp[2:-1])
        getLinks(doc, home, parent)
    except KeyboardInterrupt:
        print('Terminated by USER..Saving Crawled Links')
        finalize()
        sys.exit(0)
    return

def finalize():
    with open('crawled_links.txt', 'w+') as f:
        for href_link in href_links:
            f.write(href_link + '\n')
    print('+++ CRAWLED TOTAL href_links: [%s]' %len(href_links))

def main():
    targeturl = 'http://www.naver.com'
    home = 'http://' + targeturl.split('/')[2]
    print('+++ WEB LINK CRAWLER START > [%s]' %targeturl)
    runCrawler(home, targeturl)
    finalize()
    
if __name__ == '__main__':
    main()
    
                
        