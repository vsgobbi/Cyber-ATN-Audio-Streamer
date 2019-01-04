__author__ = 'vitor'

import socket, signal, sys

#handling exit by user
def signal_handler_server(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    #logging.error('The user exited the python packet sniffer\n')
    sys.exit(0)

print 'Press Ctrl+C if you want to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler_server)

#UDP_IP = "127.0.0.1"
UDP_IP = "172.18.64.123"
UDP_PORT = 4200
MESSAGE = "313031233134352328362c20302c20352c203529"
WIDTH = sys.getsizeof(MESSAGE)


print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "Message:", MESSAGE + "\nLenght: %d" % len(MESSAGE) + " Width: %d" % WIDTH + " bytes\n"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


"""x = 1
for n in i:
    #while True:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print "Sent %d" % n + " messages"
    sys.exit()
   """

def Attach200() :
    i = 0
    while i < 5:
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        print "Sent %d" % i + " packets"
        i += 1
    #return i


Attach200()
sys.exit(1)