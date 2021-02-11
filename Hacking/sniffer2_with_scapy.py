from scapy.all import *

protocols = {1 : 'ICMP', 6: 'TCP', 17: 'UDP'}

def showPacket(packet):
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst
    proto =packet[0][1].proto
    if proto in protocols:
        print('PROTOCOL : %s : %s -> %s' %(protocols[proto], src_ip, dst_ip))
        if proto ==1:
            print('TYPE : [%d], CODE : [%d]' %(packet[0][2].type, packet[0][2].code))
            
            
def main(filter):
    sniff(filter = filter, prn = showPacket, count =0 )
    

if __name__ == '__main__':
    filter = 'ip'
    main(filter)