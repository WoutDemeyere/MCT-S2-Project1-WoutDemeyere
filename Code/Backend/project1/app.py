# pylint: skip-file
from repositories.DataRepository import DataRepository
from modules.artnet import artnet

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS


import time
import threading

# Code voor led
from helpers.klasseknop import Button
from RPi import GPIO

led1 = 21
knop1 = Button(20)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)

node = artnet('169.254.10.1', 6454)
dmx_packet = bytearray(512)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

    socketio.emit('B2F_status_lampen', {'msg': 'Hello there'})

@socketio.on('F2B_change_pos')
def change_pos(data):
    print('change in pos')
    pos = data['pos']
    dmx_packet[1] = int(pos)

    node.send_packet('169.254.10.50', 0, 0, dmx_packet)
    #rec_dmx()


def rec_dmx():
    print('sending B2F dmx')
    packet = node.rec_packet(0,0)
    jsonify()
    #socketio.emit('B2F_dmx_packet', {'dmx_buffer':  packet})

'''
@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit')
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(lamp_id)
    if lamp_id == "2":
        lees_knop(20)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp', {'lamp': data})


def lees_knop(pin):
    print("button pressed")
    if GPIO.input(led1) == 1:
        GPIO.output(led1, GPIO.LOW)
        res = DataRepository.update_status_lamp("2", "0")
    else:
        GPIO.output(led1, GPIO.HIGH)
        res = DataRepository.update_status_lamp("2", "1")
    data = DataRepository.read_status_lamp_by_id("2")
    socketio.emit('B2F_verandering_lamp', {'lamp': data})


knop1.on_press(lees_knop)
'''

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
