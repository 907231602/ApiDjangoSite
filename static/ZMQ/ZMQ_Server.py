#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import zmq
import time
import numpy as np
np.random.seed(1520)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
import os
import sqlite3
import tensorflow as tf
from keras import backend as K
import keras
from PIL import Image
import win_unicode_console
import math
import random
win_unicode_console.enable()

context = zmq.Context()

socket = context.socket(zmq.PULL)
socket.bind('tcp://*:5558')


def insertPic(*kw):
    #kw[0]:系统名称；kw[1]:图片名称列表，
    #插入数据
    systemNames = kw[0]
    conn = sqlite3.connect('E:\\PyCharmWork\\PythonWebApp\\ApiDjangoSite\\test.db')
    c = conn.cursor()
    c.execute("DELETE from myapi_systemPic where systemName='"+systemNames+"'")
    for line in kw[1]:
        c.execute("INSERT INTO myapi_systemPic (id,systemName,picName) VALUES (NULL, '"+systemNames+"', '"+line+"')")
    conn.commit()
    print("Records created successfully")
    conn.close()

def trainDataBankHandle200(*kw):
    #kw[0]:系统名称；kw[1]:图片所在路径

    fileList=os.listdir(kw[1])  #路径下所有文件名称查询
    listType = list()
    for files in fileList:
        listType.append(files[15:])
    listType=list(set(listType))

    # 把系统名称和图片保存到数据库，格式：'银联，[贷款1,贷款2，...]'
    insertPic(kw[0], listType)  # 系统名称+图片名称

    #print(listType)
    nb_classes = listType.__len__()  #类型数量
    #print('nb_class=',nb_classes)

    X = list()
    Y = list()
    Z = list()  #one_hot数组，种类*总图片数量*每张图片被切割数量
    for lineFile in fileList:
        im=Image.open(kw[1]+"/%s" % lineFile)
        # 修改屏幕大小
        #im = screen.ScreenExpans(im)
        im_size = im.size
        Index_listType=listType.index(lineFile[15:])    #获取图片在类别图片的位置,不包括前面日期
        #print(Index_listType,'tttt==>>>',lineFile[15:])
        numX = im_size[0] / 200
        numY = im_size[1] / 200
        # 第1块           个数
        w = im_size[0] / numX  # 设置被切长度  13.66/2 的倍数
        h = im_size[1] / numY  # 设置被切宽度  7.28/2的倍数
        x = 0  # 长
        y = 0  # 宽
        count=0
        for i in range(math.ceil(numY)):  # 循环宽度（numX向上取整）次
            for j in range(math.ceil(numX)):  # 循环长度（numY向上取整）次
                region = im.crop((x, y, x + w, y + h))
                X.append(np.array(region))      #将图片切割，并把切割好的图片数组保存
                Y.append(kw[0]+'_'+lineFile.split('.')[0])  #系统名称+图片名称
                pp = np.zeros(nb_classes)
                #print('Index_listType=',Index_listType)
                pp[Index_listType] = 1
                Z.append(pp)
                #Z[Index_fileList*60+count][Index_listType]=1
                count=count+1
                x = x + w
                y = y
            x = 0  # 高依次增加，宽度从0~~边界值
            y = y + h

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    return (X, Y, Z)


#获取指定路径下测试图片，把图片切割并转化成数组,把图片对应的one_hot一起返回
def testDataBankHandle200(*kw):
    # kw[0]:系统名称；kw[1]:图片所在路径

    fileList = os.listdir(kw[1])  # 路径下所有文件名称查询
    fileAllCount = fileList.__len__()
    listType = list()
    for files in fileList:
        listType.append(files[15:])
    listType = list(set(listType))  #去除重复的字段
    nb_classes = listType.__len__()

    X = list()  #图片数组
    Y = list()  #图片名称数组
    Z = list()  #切割后图片one_hot数组
    #如果文件个数大于10，这随机选取10张图片，否则就生成一个数
    if(fileAllCount>10):
        selectFile=10
    else:
        selectFile=random.randint(1,fileAllCount)
    randomFile=random.sample(fileList,selectFile)

    #Z = np.zeros((selectFile * 4 * 7, nb_classes))  # one_hot数组

    for lineFile in randomFile:
        im = Image.open(kw[1] + "/%s" % lineFile)
        # 修改屏幕大小
        #im = screen.ScreenExpans(im)

        im_size = im.size

        Index_listType = listType.index(lineFile[15:])  # 获取图片在类别图片的位置
        #裁剪数量
        numX = im_size[0] / 200
        numY = im_size[1] / 200
        Yceil=math.ceil(numY)
        Xceil=math.ceil(numX)

        #裁剪长、宽        个数
        w = im_size[0] / numX  # 设置被切长度
        h = im_size[1] / numY  # 设置被切宽度
        x = 0  # 长
        y = 0  # 宽
        count = 0
        for i in range(Yceil):  # 循环宽度
            for j in range(Xceil):  # 循环长度
                region = im.crop((x, y, x + w, y + h))
                X.append(np.array(region))  # 将图片切割，并把切割好的图片数组保存
                Y.append(kw[0] + '_' + lineFile.split('.')[0])
                pp=np.zeros(nb_classes)
                pp[Index_listType]=1
                Z.append(pp)
                # region.save("static/imageTests/crop_average_8-%d-%d-%d.png" % (k, i, j))
                #Z[Index_fileList*Yceil*Xceil+count][Index_listType]=1
                count=count+1
                x = x + w
                y = y
            x = 0  # 高依次增加，宽度从0~~边界值
            y = y + h

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    return (X, Y, Z)

def train_cnn(*kwargs):
    #kwargs[0]:系统名称

    basePath = 'E:\\PyCharmWork\\PythonWebApp\\ApiDjangoSite\\static\\imageTrain' + '\%s' % (kwargs[0])  # 系统类别文件夹
    filesname = os.listdir(basePath)
    listType = list()
    for files in filesname:
        listType.append(files[15:].split('.')[0])  # 去除前面的时间，保留图片名称

    nb_classes = set(listType).__len__()

    # 全局变量
    img_rows, img_cols = 200, 200
    nb_filters = 32
    pool_size = (2, 2)
    kernel_size = (3, 3)
    batch_size = 18
    epochs = 1

    # model底层tensorflow的session中还有数据.
    keras.backend.clear_session()

    # the data, shuffled and split between train and tNewest sets
    (X_train, y_train, Y_train) = trainDataBankHandle200(kwargs[0], basePath)  # 系统名称+路径
    (X_test, y_test, Y_test) = testDataBankHandle200(kwargs[0], basePath)

    # 根据不同的backend定下不同的格式
    if K.image_dim_ordering() == 'th':
        X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    # 构建模型
    model = Sequential()
    model.add(Convolution2D(nb_filters, (kernel_size[0], kernel_size[1]),
                            padding='same',
                            input_shape=input_shape))  # 卷积层1
    model.add(Activation('relu'))  # 激活层
    model.add(Convolution2D(nb_filters, (kernel_size[0], kernel_size[1])))  # 卷积层2
    model.add(Activation('relu'))  # 激活层
    model.add(MaxPooling2D(pool_size=pool_size))  # 池化层
    model.add(Dropout(0.25))  # 神经元随机失活
    model.add(Flatten())  # 拉成一维数据
    model.add(Dense(128))  # 全连接层1
    model.add(Activation('relu'))  # 激活层
    model.add(Dropout(0.5))  # 随机失活
    model.add(Dense(nb_classes))  # 全连接层2
    model.add(Activation('softmax'))  # Softmax评分

    # 编译模型
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    # 训练模型
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
              verbose=1, validation_data=(X_test, Y_test))

    # 评估模型
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    model.save('E:\\PyCharmWork\\PythonWebApp\\ApiDjangoSite\\static\\h5\\%s.h5' % kwargs[0])


while True:
    data = socket.recv()
    train_cnn(data.decode('utf-8'))

    print(data.decode('utf-8'))





