#sniffer0.py는 패킷 하나를 스니핑하면 화면에 결과를 출력하고 종료하는 프로그램이다. 
#그걸 조금 수정하여 사용자가 ctrl+c를 누를 때까지 패킷을 지속적으로 스니핑할수 있도록 하고, 스니핑 된 패킷에서 IP해서 부분만 화면에 출력하는 코드로 바꾸어 보자.

from socket import *
import os

def recvData(sock):            #소켓으로부터 패킷을 수신하는 부분을 별도의 함수인 recvData(sock)으로 구현한다.
    data = ''
    try:
        data = sock.recvfrom(65565)
    except timeout:            #socket 타임아웃 예외가 발생하면 변수 data에 빈 문자열을 담는다
        data = ''
    return data[0]            #수신한 패킷의 첫 번째 멤버를 리턴한다. 이는 패킷스니핑결과에서 설명한 바와 같이 첫 번쨰 멤버인 바이트 코드에 우리가 해석하고자 하는 IP헤더가 포함되어 있기 때문

def sniffing(host):
    if os.name == 'nt':
        sock_protocol = IPPROTO_IP
    else :
        sock_protocol = IPPROTO_ICMPV6
    
    sniffer = socket(AF_INET, SOCK_RAW, sock_protocol)
    sniffer.bind((host,0))
    
    sniffer.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    if os.name == 'nt':
        sniffer.ioctl(SIO_RCVALL, RCVALL_ON)
    
    count=1
    try:
        while True:
            data = recvData(sniffer)
            print('SNIFFED [%d] %s' %(count, data[:20]))  # data[:20]은 IP헤더
            count+=1
    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)
            
def main():
    host = gethostbyname(gethostname())
    print('START SNIFFING at [%s]' %host)
    sniffing(host)
    
if __name__ == '__main__':
    main()