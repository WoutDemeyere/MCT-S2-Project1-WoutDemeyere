import socket

OpCodes = {'OpPoll':0x2000, 'OpPollReply':0x2100, 'OpAddress':0x6000, 'OpInput':0x7000, 'OpDMX':0x5000, 'OpNzs':0x5100, 'OpSync':0x5200}

ARTNET_HEADER = 'Art-Net'


class artnet:
    def __init__(self, UDP_PORT, UDP_IP):
        self.UDP_PORT = UDP_PORT
        self.UDP_IP = UDP_PORT
        self.UDP_IP_to = "192.168.1.69"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', self.UDP_PORT))

        self.SENDER_IP = 0

        self.Header = ''
        self.OpCode = 0
        self.ProtVer = 0

        self.packet = 0
        self.address = 0

        self.DMX_Packet = False
        self.dmx_buffer = []

        self.dmx_buffer_send = []

        self.ArtDMX_packet = []

        for i in range(530):
            self.dmx_buffer.append(0)

        for i in range(512):
            self.dmx_buffer_send.append(0)

        for i in range(18):
            self.ArtDMX_packet.append(0)


    def decode_packet(self):
        self.packet, self.address = self.sock.recvfrom(1024)

        self.Header = self.packet[0:7].decode('ascii')
        self.OpCode = hex((self.packet[9] << 8) | self.packet[8])

        #sProtVers_hex = self.packet[10:12]
	    #self.ProtVer = int.from_bytes(ProtVers_hex, byteorder='big')
        

        if self.Header == ARTNET_HEADER:
            #if self.OpCode in OpCodes:

            if self.OpCode == hex(OpCodes['OpPoll']):
                self.DMX_Packet = False
                self.ArtnetPollReply()
            
            elif self.OpCode == hex(OpCodes['OpDMX']):
                self.DMX_Packet = True
            #else:
                #print('WRONG OPCODE')

    def ArtnetPollReply(self):
        pass
    
    def read_dmx_packet(self, subnet, univer):             
        self.decode_packet()    #--- Decode packet not needy

        if self.DMX_Packet == True:

            self.sub = self.packet[14] & 0xF0   #--- Something wrong with byte of pack:14
            self.uni = self.packet[14] & 0x0F
            
            length_hex = self.packet[16:18]
            self.length = int.from_bytes(length_hex, byteorder='big')

            print(self.sub, self.uni)
            
            print(self.packet[529])
            if subnet == self.sub and self.uni == univer:
                for i in range(self.length):
                    #print(self.packet[i])
                    self.dmx_buffer[i] = self.packet[i+18]
            elif subnet != self.sub or self.uni != univer:
                for i in range(self.length):
                    self.dmx_buffer[i] = 0         
        
            return self.dmx_buffer


    def read_dmx_channel(self, subnet, univer, chan):     
        assert subnet >= 0 and subnet <= 15    
        assert univer >= 0 and univer <= 15     
        assert chan >= 0 and chan <= 512

        self.decode_packet()    #--- Decode packet not needy

        chan_val = 0

        if self.DMX_Packet == True:

            self.sub = self.packet[14] & 0xF0   #--- Something wrong with byte of pack:14
            self.uni = self.packet[14] & 0x0F

            print(self.sub, self.uni)
            
            print(self.packet[529])
            if subnet == self.sub and self.uni == univer:
                chan_val = self.packet[chan+18]
            elif subnet != self.sub or self.uni != univer:
                chan_val = 0
        
            return chan_val
    
    def send_dmx_channel(self, subnet, univer, chan, val):
        assert subnet >= 0 and subnet <= 15    
        assert univer >= 0 and univer <= 15     
        assert chan >= 0 and chan <= 512

        for i in range(512):
            if i == chan:
                self.dmx_buffer_send[i] = val

        #Art-Net Header
        for i in range(0,7):
            self.ArtDMX_packet[i] = ARTNET_HEADER[i]

        #OpCode
        self.ArtDMX_packet[8] = OpCodes['OpDMX'] & 0x0F
        self.ArtDMX_packet[9] = OpCodes['OpDMX'] & 0xF0

        #ProtVers
        self.ArtDMX_packet[10] = 0
        self.ArtDMX_packet[11] = 14

        #Sequence
        self.ArtDMX_packet[12] = 0

        #Physical
        self.ArtDMX_packet[13] = 0

        #Subnet
        self.ArtDMX_packet[14] = subnet

        #Univer
        self.ArtDMX_packet[15] = univer

        #Length
        self.ArtDMX_packet[16] = 0x2000 & 0xF0
        self.ArtDMX_packet[17] = 0x2000 & 0x0F

        #DMX packet
        self.ArtDMX_packet[17] = self.dmx_buffer_send

        for data in self.ArtDMX_packet:
            data = str(data)
            self.sock.sendto(data.encode(), (self.UDP_IP_to, self.UDP_PORT))




if __name__ == "__main__":

    node = artnet(6454, '192.168.1.69')

    while 1:

        print(node.send_dmx_channel(0,0,5,127))
    