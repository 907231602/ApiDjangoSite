#!/usr/bin/env python3.5.2
#coding=utf-8

import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUSH)

socket.bind('tcp://*:5557')

while True:
    # data = input('input your data:')
    #
    # socket.send(data.encode('utf-8'))
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send("%i %i %i" % (zipcode, temperature, relhumidity))