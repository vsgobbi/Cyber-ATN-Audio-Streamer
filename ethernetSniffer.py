__author__ = 'vitor'

#!/usr/bin/env python

'''
 Created at ICEA (Brazilian Airspace Control Institute)
 Vitor Sgobbi, 2015
 This is part of Cyber Range ATN Testbed
 Python Packet Sniffer module
 ethernetSniffer handles TCP, ICMP and UDP protocols
'''

import socket, sys, signal
from struct import *

#convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b

#create a AF_PACKET type raw socket
#define ETH_P_ALL 0x0003    /* For Every packet */
try:
    s = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
except socket.error, msg:
    print 'Socket could\'n t be created, error: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


#handling exit by user
def signal_handler_server(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    #logging.error('The user exited the python packet sniffer\n')
    sys.exit(0)

print 'Press Ctrl+C if you want to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler_server)

#receive packets
while True:
    packet = s.recvfrom(65565) #receive from all ports

    packet = packet[0]

    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header) #'!6s6sH' ??
    eth_protocol = socket.ntohs(eth[2])
    print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)

#Parse IP and protocol number
    if eth_protocol == 8 :
        #the 20 first characters are the ip header
        ip_header = packet[eth_length:20+eth_length]

#unpack header
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        print 'Version: ' + str(version) + ' IP Header Length: ' + str(ihl) + ' TTL: ' + str(ttl) + ' Protocol: ' \
          + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address: ' + str(d_addr)


#TCP protocol
    if protocol == 6 :
        t = iph_length + eth_length
        tcp_header = packet[t:t+20]

        #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header)

        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4

        print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

        h_size = eth_length + iph_length + tcph_length * 4
        data_size = len(packet) - h_size

        #get data from the packet
        data = packet[h_size:]

        print 'Data : ' + data

#ICMP Packets
    elif protocol == 1 :
        u = iph_length + eth_length
        icmph_length = 4
        icmp_header = packet[u:u+4]

#now unpack them :)
        icmph = unpack('!BBH' , icmp_header)

        icmp_type = icmph[0]
        code = icmph[1]
        checksum = icmph[2]

        print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)

        h_size = eth_length + iph_length + icmph_length
        data_size = len(packet) - h_size

#get data from packet
        data = packet[h_size:]

        print 'Data : ' + data


#UDP packets
    elif protocol == 17 :
        u = iph_length + eth_length
        udph_length = 8
        udp_header = packet[u:u+8]

        udph = unpack('!HHHH', udp_header)
        source_port = udph[0]
        dest_port = udph[1]
        length = udph[2]
        checksum = udph[3]

        print 'Source Port: ' + str(source_port) + ' Destination Port: ' + str(dest_port) + ' Length : ' + str(length)\
              + ' Checksum: ' + str(checksum)

        h_size = eth_length + iph_length + udph_length
        data_size = len(packet) - h_size

        #get data from playload
        #do dissector here!
        data = packet[h_size]
        print 'Data: ' + data

        #print some other IP packet like IGMP
    else :
        print 'Protocol other than TCP/UDP/ICMP'

    print