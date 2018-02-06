#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import zmq
#中间件，负责发送
context = zmq.Context()

recive = context.socket(zmq.PULL)
recive.connect('tcp://127.0.0.1:5557')

sender = context.socket(zmq.PUSH)
sender.connect('tcp://127.0.0.1:5558')

while True:
    data = recive.recv()
    sender.send(data)