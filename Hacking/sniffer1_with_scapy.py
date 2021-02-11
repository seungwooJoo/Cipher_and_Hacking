from scapy.all import *

def showPacket(packet):
    print(packet.show())    #packet.show()는 캡처한 패킷을 사람이 알아볼 수 있는 정보로 변환해 줍니다. 
    
def main(filter):
    sniff(filter = filter, prn = showPacket, count = 1)

    
# filter : 원하는 패킷만 볼 수 있는 필터를 저장합니다.
# prn : 캡처한 패킷을 처리하기 위한 함수를 지정합니다. 지정한 함수의 인자는 캡처한 패킷으로 정해집니다. 
# count : 패킷을 캡처하는 횟수를 지정합니다. 0이면 사용자가 중지할 때까지 캡처합니다. 

#sniff()가  showPacket()을 호출할 떄 이 함수의 인자인 packet에 캡처한 패킷을 자동으로 넘겨줍니다.
    
if __name__ == '__main__':
    filter = 'ip'
    main(filter)
    
