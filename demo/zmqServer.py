#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-



import zmq
import time

context = zmq.Context()

socket = context.socket(zmq.PULL)
socket.bind('tcp://*:5558')

while True:
    data = socket.recv()
    time.sleep(5)

    print(data.decode('utf-8'))

