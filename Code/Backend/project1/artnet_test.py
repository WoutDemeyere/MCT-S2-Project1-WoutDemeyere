from modules.artnet import artnet

node = artnet('169.254.10.1', 6454)

while 1:

    node.send_channel('169.254.10.50', 0, 0, 23, 255)

    print(node.rec_packet(0,0))