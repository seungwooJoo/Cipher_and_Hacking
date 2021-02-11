from socket import *
from netaddr import IPNetwork, IPAddress

def sendMsg(subnet, msg):
    sock = socket(AF_INET, SOCK_DGRAM)        #UDP소켓을 생성합니다.
    for ip in IPNetwork(subnet):
        try:
            print('SENDING MESSAGE TO [%s]' %ip)
            sock.sendto(msg.encode('utf-8'), ('%s' %ip, 9000))
        except Exception as e:
            print(e)
            
            
def main():
    host = gethostbyname(gethostname())
    subnet = host + '/24'
    msg = 'KNOCK!KNOCK!'
    sendMsg(subnet, msg)
    
if __name__ == '__main__':
    main()

# from socket import *
# from netaddr import IPNetwork, IPAddress

# def sendMsg(subnet, msg):
#     sock = socket(AF_INET, SOCK_DGRAM)        #UDP소켓을 생성합니다.:
#     try:
#         print('SENDING MESSAGE TO 172.17.0.38...' )
#         sock.sendto(msg.encode('utf-8'), ('172.17.0.38', 9000))
#     except Exception as e:
#         print(e)
            
            
# def main():
#     host = gethostbyname(gethostname())
#     subnet = host + '/16'
#     msg = 'KNOCK!KNOCK!'
#     sendMsg(subnet, msg)
    
# if __name__ == '__main__':
#     main()