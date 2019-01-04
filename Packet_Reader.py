__author__ = 'vitor'

from datetime import datetime
from impacket import ImpactDecoder
import pcapy
import csv, signal, sys
import SocketServer


#handling exit by user
def signal_handler_server(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    #logging.error('The user exited the python packet sniffer\n')
    sys.exit(0)

print 'Press Ctrl+C if you want to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler_server)

def GetPayload(tcpHeader):
    payload_decimal = tcpHeader.child().get_bytes().tolist()
    ascii = [] #create list to store ASCII content
    for decByte in payload_decimal: #iterate throught the whole payload
        if decByte in range(9,14) or decByte in range(32, 127): #only get decimal ranges of 9-13 and 32-126
            hexByte = str(hex(decByte)).lstrip("0x") #convert decimal to hex string and remove all "0x" from beginning
            if len(hexByte) == 1:
                hexByte = "0" + hexByte #fill hex value with 0 if it is one digit number
            asciiByte = hexByte.decode('hex') #convert hex to ASCII
            ascii.append(asciiByte) #add ASCII to ASCII list
    payload_ascii=".join(ascii)" #store payload as string

    return payload_ascii


def Process (header,data):
    decoder = ImpactDecoder.EthDecoder()
    ether = decoder.decode(data)
    ipHeader = ether.child()
    packetType = ipHeader.child().protocol #UDP = 17, TCP = 6, ICMP = 1

    if packetType == 17 :
        tcpHeader = ipHeader.child()
    if (tcpHeader.get_PSH() and tcpHeader.get_ACK() and tcpHeader.get_th_dport() == 4444 or \
        tcpHeader.get_th_sport() == 4444):
        payload = GetPayload(tcpHeader)
        print payload + "\n"
    return


packetReader = open("packetsFile.pcap")
packetReader.loop(0, Process)


def nodeStateCheckout(nodeid, state, nodeState):
    if (state == ord(nodeState)):
        return "OK"
    else:
        return "FAIL"

def timeConstructor(time):

    year = str(ord(time[0]) << 8 | ord(time[1]))
    month = str(ord(time[2]))
    day = str(ord(time[3]))
    hour = str(ord(time[4]))
    minute = str(ord(time[5]))
    second = str(ord(time[6]))

    time_formatted = year + "-" + month + "-" + day \
                     + " " + hour + ":" + minute + ":" + second
    print time_formatted
    return time_formatted


class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    #timeConstructor(time=1)
    def handle(self):

        try:

            data = self.request[0].strip()
            socket = self.request[1]
            print "{} wrote:".format(self.client_address[0])

            pkg_type = ord(data[0])

            if pkg_type == 1:      #what kind? # log 3

                state = ord(data[1])
                csvfile = open("log3.csv", "a+") #need file?
                csvwriter = csv.writer(csvfile, delimiter=',')
                time_reconstructed = timeConstructor(data[2:9])
                if csvfile.open == None:
                    print "There is no csvfile!"
                if state == 3:
                    csvwriter.writerow(["STOP", time_reconstructed])
                elif state == 2:
                    csvwriter.writerow(["START", time_reconstructed])
                else:
                    print "unknown state"

                csvfile.close()

            else:
                print "packet not known"

        except IndexError:
            print "Bad parsed byte"


if __name__ == "__main__":
    HOST, PORT = "localhost", 46827
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
    print "Port = " + PORT