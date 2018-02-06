#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

#训练图片，图片大小（1920*1080）


import numpy as np
np.random.seed(1520)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
#import keras

from . import picHandle
import os

import tensorflow as tf
from keras import backend as K

#import gc
#安装pip install  win_unicode_consoles
import win_unicode_console
win_unicode_console.enable()
#http://blog.csdn.net/lujiandong1/article/details/55806435


#kwargs[0]:系统名称
def Cnn_run(*kwargs):
    sess = tf.Session()
    K.set_session(sess)

    basePath='static/imageTrain'+'/%s' % (kwargs[0])  #系统类别文件夹
    filesname=os.listdir(basePath)
    listType=list()
    for files in filesname:
        listType.append(files[15:].split('.')[0])    #去除前面的时间，保留图片名称

    nb_classes=set(listType).__len__()



    # 全局变量
    img_rows, img_cols =200,200
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    pool_size = (2, 2)
    # convolution kernel size
    kernel_size = (3, 3)
    batch_size = 18
    epochs = 1

    #model底层tensorflow的session中还有数据.
    #keras.backend.clear_session()
    K.clear_session()

    # the data, shuffled and split between train and tNewest sets
    (X_train, y_train,Y_train) = picHandle.trainDataBankHandle200(kwargs[0],basePath) #系统名称+路径
    (X_test, y_test,Y_test) = picHandle.testDataBankHandle200(kwargs[0],basePath)




    # 根据不同的backend定下不同的格式
    if K.image_dim_ordering() == 'th':
        X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        X_train =X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
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
    score=model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    model.save('static/h5/%s.h5' % kwargs[0])

    #gc.collect()






