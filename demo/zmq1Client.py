#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import zmq

context = zmq.Context()
print('connect to hello world server')
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
request=0
while True:
    request=request+1
    print('send ', request, '...')
    socket.send('hello'.encode('utf-8'))
    message = socket.recv()
    print('received reply ', request, '[', message, ']')
