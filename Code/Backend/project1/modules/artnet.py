import socket
from .ArtPackets import ArtPacket
import threading

OpCodes = {'OpPoll':0x2000, 'OpPollReply':0x2100, 'OpAddress':0x6000, 'OpInput':0x7000, 'OpDMX':0x5000, 'OpNzs':0x5100, 'OpSync':0x5200}

class artnet:
    def __init__(self, UDP_IP, UDP_PORT):
        self.UDP_PORT = UDP_PORT
        self.UDP_IP_LOCAL = UDP_IP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.UDP_IP_LOCAL, self.UDP_PORT))

        self.dmx_packet = bytearray(512)

        self.rec_ip = '169.254.10.50'

        #self.artpollcheck = threading.Thread(self.check_ArtPoll)
 

    def decode_packet(self, packet):
        #packet = list(packet)
        #print(len(packet))
        opcode = hex((packet[9] << 8) | packet[8])
        return opcode

    def rec_packet(self, uni, sub):
        rec_data, self.rec_ip = self.socket.recvfrom(1024)
        print(rec_data)

        OpCode = self.decode_packet(rec_data)

        if OpCode == OpCodes['OpDMX']:
            seq, phy, subn, univ, length, dmx_buffer = ArtPacket.decode_ArtDMX(rec_data)

            if sub == subn and uni == univ:
                return dmx_buffer
        else:
            pass

    def rec_channel(self, uni, sub, chan):
        rec_data, self.rec_ip = self.socket.recvfrom(1024)

        self.type = self.decode_packet(rec_data)

        if self.type == OpCodes['OpDMX']:
            seq, phy, subn, univ, length, dmx_buffer = ArtPacket.decode_ArtDMX(rec_data)

            if sub == subn and uni == univ:
                for i in range(length):
                    if i == chan:
                        return dmx_buffer[i]
        else:
            pass
            
    def send_packet(self, ip, uni, sub, packet):
        encoded_packet = ArtPacket.encode_ArtDMX(sub, uni, len(packet), packet)
        self.socket.sendto(encoded_packet, (ip, self.UDP_PORT))

    def send_channel(self, ip, uni, sub, chan, val):

        for i in range(512):
            if i == chan:
                self.dmx_packet[i] = val

        encoded_packet = ArtPacket.encode_ArtDMX(sub, uni, len(self.dmx_packet), self.dmx_packet)
        self.socket.sendto(encoded_packet, (ip, self.UDP_PORT))
    
    def send_ArtPoll(self):
        ArtPollPacket = ArtPacket.encode_ArtPoll()
        self.socket.sendto(ArtPollPacket, ('', self.UDP_PORT))

    def send_ArtPollReply(self):
        ArtPollReplyPacket = ArtPacket.encode_ArtPollReply(self.UDP_IP_LOCAL, 6454, )

    def check_ArtPoll(self):
        rec_data, self.rec_ip = self.socket.recvfrom(1024)
        OpCode = self.decode_packet(rec_data)

        if OpCode == OpCodes['OpArtPoll']:
            self.send_ArtPollReply()
        

    def get_ip(self):
        return self.rec_ip
        

if __name__ == '___main__':
    node = artnet('192.168.1.100', 6454)

    while 1:
        node.send_channel('192.168.1.200', 0, 0, 3, 100)