#이 코드가 실행되는 컴퓨터에 송수신되는 패킷 하나를 가로채서 그 내용을 화면에 출력하는 코드
#sniffer0.py는 시스템의 중요한 부분을 변경하는 것이므로 윈도우에서는 관리자 권한을, 리눅스 계열에서는 루트권한을 가지고 실행해야 합니다. 
from socket import *
import os

def sniffing(host):
    if os.name == 'nt':        #윈도우인 경우
        sock_protocol = IPPROTO_IP
    else: 
        sock_protocol = IPPROTO_ICMP
        
    #sock_protocol은 소켓을 생성할 때 프로토콜을 지정하는 세 번째 인자로 사용된다.
    #윈도우는 프로토콜에 관계없이 들어오는 모든 패킷을 가로채기 때문에 IP를 지정해도 무관하지만, 유닉스나 리눅스는 ICMP를 가로채겠다는 것을 명시적으로 표시해야 합니다.
    sniffer = socket(AF_INET, SOCK_RAW, sock_protocol)    #sock_protocol로 지정된 프로토콜을 이용하는 Raw소켓을 만들고,
    sniffer.bind((host,0))                                #그걸 호스트와 바인드합니다. 바인드함으로써 소켓을 통해 들어오는 네트워크 패킷을 수신할 준비를 마칩니다. 
    sniffer.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)        #가로채는 패킷에 IP헤더를 포함하라고 소켓의 옵션으로 지정합니다.
    
    if os.name == 'nt':
        sniffer.ioctl(SIO_RCVALL, RCVALL_ON)
    packet = sniffer.recvfrom(65565)  #recvfrom(65565)는 소켓으로 패킷이 들어올 떄 까지 대기합니다.
    print(packet)
    
    if os.name == 'nt':
        sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

        
def main():
    host = gethostbyname(gethostname())     #gethostbyname()은 호스트이름을 IPv4형식으로 바꾼다. socket 모듈의 gethostname()은 현재 호스트의 이름을 리턴한다.
    #따라서 변수 host는 sniffer0.py가 구동되는 컴퓨터의 IP주소가 담기게 된다. 
    print('START SNIFFING at [%s]' %host)
    sniffing(host)                #패킷 스니핑 실시 
    
if __name__ == '__main__':
    main()