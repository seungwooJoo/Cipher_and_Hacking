from scapy.all import *

sniff(prn=lambda x: print(x), count=1)

#Scapy를 이용하면 패킷 스니핑을 매우 쉽게 구현할 수 있다. 
#Scapy를 이용하면 단 1줄로 sniffer0.py와 비슷한 기능을 수행하는 패킷 스니퍼를 구현할 수 있다. 
#count 는 패킷은 캡처하는 횟수를 지정한다. 0이면 사용자가 중지할 때 까지 캡처한다. 