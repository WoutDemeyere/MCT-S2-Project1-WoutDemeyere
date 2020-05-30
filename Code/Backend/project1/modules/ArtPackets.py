class ArtPacket:

    # ----- Need to add protver chek (Maybe OpCode 2)
    @staticmethod
    def decode_ArtDMX(packet):

        dmx_buffer = bytearray()

        for i in range(512):
            dmx_buffer.append(0)

        sequence = packet[12]
        physical = packet[13]

        subnet = packet[14] & 0xF0
        univer = packet[14] & 0x0F

        len_hex = packet[16:18]
        length = int.from_bytes(len_hex, byteorder='big')

        for i in range(length):
            dmx_buffer[i] = packet[i+17]         #Make this cleaner

        return sequence, physical, subnet, univer, length, dmx_buffer
    
    @staticmethod
    def encode_ArtDMX(sub, uni, length, dmx_data):
        assert sub >= 0 and sub <= 15    
        assert uni >= 0 and uni <= 15     
        
        packet_buffer = bytearray()

        packet_buffer.extend(bytearray('Art-Net', 'utf-8'))
        packet_buffer.append(0x0)

        # --- OpCode
        packet_buffer.append(0x00)
        packet_buffer.append(0x50)

        # --- Protver
        packet_buffer.append(0x00)
        packet_buffer.append(14)

        # --- Sequence
        packet_buffer.append(0x00)

        # --- Physical
        packet_buffer.append(0x00)

        # --- Subnet
        packet_buffer.append(sub)

        # --- Universe
        packet_buffer.append(uni)

        # --- length
        packet_buffer.append(0x20)
        packet_buffer.append(0x0)

        # --- DMX PACKET
        packet_buffer.extend(dmx_data)

        return packet_buffer
    
    @staticmethod
    def encode_ArtPoll():
        packet_buffer = bytearray()

        packet_buffer.extend(bytearray('Art-Net', 'utf-8'))
        packet_buffer.append(0x0)

        # --- OpCode
        packet_buffer.append(0x00)
        packet_buffer.append(0x50)

        # --- Protver
        packet_buffer.append(0x00)
        packet_buffer.append(14)

        # --- Flags
        packet_buffer.append(0x00)

        # --- Priority
        packet_buffer.append(0x00)

        return packet_buffer