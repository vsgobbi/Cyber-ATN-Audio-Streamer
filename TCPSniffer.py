__author__ = 'vitor'

#!/usr/bin/env python

'''
 Created at ICEA (Brazilian Airspace Control Institute)
 Vitor Sgobbi, 2015
 This is part of Cyber Range ATN Testbed
 Python Packet Sniffer module
 This sniffer handles UDP payloads
'''
# Source: http://www.binarytides.com/python-packet-sniffer-code-linux/
#Packet sniffer in python
#For Linux

import socket, socket, sys, signal
from struct import *


#handling exit by user
def signal_handler_server(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    #logging.error('The user exited the python packet sniffer\n')
    sys.exit(0)

print 'Press Ctrl+C if you want to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler_server)

try:
    #create an INET, raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ntohs(0x0003)) #sniff all data instead only TCP packets
    #s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) #uncomment to sniff only UDP packets
except socket.error, msg:
    print 'Socket could\'n t be created, error: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()




# receive a packet
while True:
    packet = s.recvfrom(65565)
    #print s.recvfrom(3030)

    packet = packet[0]

    #separate 20 characters for the ip header index
    ip_header = packet[0:20]

    #unpack header
    iph = unpack('!BBHHHBBH4s4s', ip_header)

    #versionate IPv4
    version_ip = iph[0]
    version = version_ip >> 4
    ip = version_ip & 0xF # 4 hex

    ip_length = ip * 4

    ttl = iph[5]
    protocol = iph[6]
    #socket address
    socket_address = socket.inet_ntoa(iph[8]);
    #d address?
    d_address = socket.inet_ntoa(iph[9]);

    print 'IP Version : ' + str(version) + ' IP Header Lenght : ' + str(ip) \
          + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' \
          + str(socket_address) + ' Destination Address : ' + str(d_address)

    tcp_header = packet[ip_length:ip_length+20]

    #unpack header
    tcph = unpack('!HHLLBBHHH', tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4

    print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' \
          + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)

    h_size =  ip_length + tcph_length * 4
    data_size = len(packet) - h_size

    #get data from the packet
    data = packet[h_size:]

    print 'Data : ' + data
    #print '\n'

    #unpack UDP packets
