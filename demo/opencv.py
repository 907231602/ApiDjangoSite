#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import cv2
import numpy as  np

img = cv2.imread('../static/image/hello.png')
cv2.imshow('img', img)
k = cv2.waitKey(0)


def img_tostring(img):  # input a img np.array
    ret, jpeg = cv2.imencode('.jpg', img)
    if ret == True:
        stri = jpeg.tostring()
        return stri


def string_toimg(stri):
    print('===>',stri)
    jpeg = np.array(stri)
    img = cv2.imdecode(jpeg, 1)
    if img:
        return img
cv2.imshow('img', img)
cv2.waitKey(0)
