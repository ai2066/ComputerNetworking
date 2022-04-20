from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii
 
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
 
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string):
    # In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
 
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
 
def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
	ID = 11238
	myChecksum = 0
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	myChecksum = checksum(header + data)
	myChecksum = socket.htons(myChecksum)
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this

    	packet = header + data
    	return packet
 
def get_route(hostname):
    timeLeft = TIMEOUT
	tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces
	
    for ttl in xrange(1,MAX_HOPS):
        for tries in xrange(TRIES):
            destAddr = socket.gethostbyname(hostname)
            #Fill in start
            # Make a raw socket named mySocket
            icmp =socket.getprotobyname("icmp")
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            #Fill in end
            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                sSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                timeInSelect = (time.time() - sSelect)
                if whatReady[0] == []:
                    print "   *         *            *          Request timed out."
                receivedPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - timeInSelect
                if timeLeft <= 0:
                    print "   *         *            *          Request timed out."
            except socket.timeout:
                continue
 
            else:
                #Fill in start
                # Fetch the icmp type from the IP packet                
                icmpHeader = receivedPacket[20:28]
                type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                #Fill in end
                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", receivedPacket[28:28 + bytes])[0]
                    print "   %d     rtt=%.0f ms    %s" % (ttl, (timeReceived - t)*1000, addr[0])
 
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", receivedPacket[28:28 + bytes])[0]
                    print "   %d     rtt=%.0f ms    %s" % (ttl, (timeReceived - t)*1000, addr[0])
 
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", receivedPacket[28:28 + bytes])[0]
                    print "   %d     rtt=%.0f ms    %s" % (ttl, (timeReceived - t)*1000, addr[0])
                    return
                else:
                    print " ERROR "
                break
 
            finally:
                mySocket.close()
				
if __name__ == '__main__':
	get_route("google.co.il")
	
