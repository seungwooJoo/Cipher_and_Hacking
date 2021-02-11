from socket import *
import os
import struct

def parse_ipheader(data):        # 소켓으로부터 수신한 데이터를 인자로 입력받은 후 20바이트 IP헤더를 파이썬 튜플 자료형으로 변환하기 위한 함수입니다. 
    ipheader = struct.unpack('!BBHHHBBH4s4s', data[:20])    #data[:20]을 첫 번쨰 인자인 포맷 문자열에 맞게 변환한 후 파이썬 튜플로 리턴한다. 
    return ipheader

# !BBHHHBBH4s4s는 네트워크 바이트 순서로 1,1,2,2,2,1,1,2,4,4 바이트로 구분하라는 뜻이다. 

def getDatagramSize(ipheader):
    return ipheader[2]

def getProtocol(ipheader):
    protocols = {1:'ICMP', 6:'TCP', 17:'UDP'}
    proto = ipheader[6]
    if proto in protocols:
        return protocols[proto]
    else:
        return 'OTHERS'

def getIP(ipheader):
    src_ip = inet_ntoa(ipheader[8])    #inet_ntoa() : 바이트 문자열을 우리가 익숙한 IP주소 형식으로 변환해줌.
    dest_ip = inet_ntoa(ipheader[9])
    return (src_ip, dest_ip)


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
            ipheader = parse_ipheader(data[:20])
            datagramSize = getDatagramSize(ipheader)
            protocol = getProtocol(ipheader)
            src_ip, dest_ip = getIP(ipheader)
            
            print('\nSNIFFED [%d] +++++++++++++++++++' %count)
            print('Datagram SIZE : \t%s' %str(datagramSize)) #byte
            print('Protocol:\t%s ' % protocol)
            print('Source IP : \t%s' %src_ip)
            print('Destination IP : \t%s' %dest_ip)
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