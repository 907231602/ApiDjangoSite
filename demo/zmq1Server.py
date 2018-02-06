#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')

while True:
    message = socket.recv()
    print('received request: ', message)

    time.sleep(5)
    socket.send('World'.encode('utf-8'))