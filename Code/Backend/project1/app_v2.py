from repositories.DataRepository import DataRepository
from modules.artnet import artnet

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS


import time
import threading

node = artnet('169.254.10.1', 6454)
dmx_packet = bytearray(512)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

takel_ip = '169.254.10.50'

@socketio.on('connect')
def initial_connection():
    print('A new client connect')

    socketio.emit('B2F_status_lampen', {'msg': 'Hello there'})

@socketio.on('F2B_change_pos')
def change_pos(data):
    print('change in pos')
    pos = data['pos']
    node.send_channel(takel_ip, 0, 0, 1, int(pos))
    #DataRepository.update_curr_pos(1, int(pos))

@socketio.on('F2B_move')
def move_takel(data):
    dr = data['mv']

    print(dr)

    if dr == 'up':
        print('moving up')
        node.send_channel(takel_ip, 0, 0, 50, 56)
    elif dr == 'down':
        print('moving down')
        node.send_channel(takel_ip, 0, 0, 51, 56)
    elif dr == 'none':
        node.send_channel(takel_ip, 0, 0, 50, 0)
        node.send_channel(takel_ip, 0, 0, 51, 0)

@socketio.on('F2B_set_start')
def set_start(data):
    start = data['start']
    
    if start:
        print('setting start')
        node.send_channel(takel_ip, 0, 0, 40, 56)
    else:
        socketio.emit('B2F_new_start', {'slider_val': 0})
        node.send_channel(takel_ip, 0, 0, 40, 0)

@socketio.on('F2B_set_end')
def set_end(data):
    start = data['end']
    
    if start:
        print('setting end')
        node.send_channel(takel_ip, 0, 0, 41, 56)
    else:
        socketio.emit('B2F_new_end', {'slider_val': 255})
        node.send_channel(takel_ip, 0, 0, 41, 0)
    

@socketio.on('F2B_give_ip')
def get_ip(data):
    print('Giving IP')
    
    ip = node.get_ip()
    DataRepository.update_ip(1, ip)
    socketio.emit('B2F_takel_ip', {'ip': ip}) #(5)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
