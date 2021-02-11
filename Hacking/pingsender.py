import os
from netaddr import IPNetwork, IPAddress
from socket import *
from threading import Thread

def sendPing(ip):
    try:
        ret = os.system('ping -n 1 %s' %ip)
    except Exception as e:
        print(e)
        
def main():
    host = gethostbyname(gethostname())
    subnet = host + '/24'
    for ip in IPNetwork(subnet):
        t=Thread(target=sendPing,args=(ip,))
        t.start()
        
if __name__ == '__main__':
    main()
    
#sendPing(ip) 는 시스템의 ping명령을 직접 호출하여 해당 아이피로 ping을 1회 전송한다. 
# 256개 서브네트워크 아이피에 대해 ping을 순차적으로 실행하면 너무 느리므로,
# 서브네트워크 ip개수만큼 스레드를 구동하여 처리속도를 높인다. 