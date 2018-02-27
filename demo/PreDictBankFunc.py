#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

import myApi.picHandle as picHandle
import myApi.ResultAnalysis as analysisType
from PIL import Image
import numpy as np
from keras import backend as K
from keras.models import load_model
import time
import os

import tensorflow as tf

#对图片进行预测，把图片切割数组化，对预测后的值进行估测，大于0.5图片概率比较高，小于0.5的概率舍弃
#对概率结果进行统计，大于切割图片张数一半减1的为该类型，否则舍弃
models = load_model('D:/windows/ApiDjangoSite/static/h5/智联招聘.h5')
g = tf.get_default_graph()
#图片数组，图片名称
def predictBank(ar):
    #g=tf.Graph()

    with g.as_default():
        #sess=tf.Session(graph=g)  #把识别需要的数据放在自己创建的Graph,Session，避免使用默认Graph,造成数据错误
        #with sess.as_default():
        img_rows, img_cols = 200, 200
        time1 =  time.time()
        (X_test, y_test) = picHandle.testPredictDataHandle200(ar)
        time2 = time.time()
        print("picHandle:")
        print(time2-time1)
        ar.close()  #关闭打开的图片资源
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
        X_test = X_test.astype('float32')
        X_test /= 255
        time3= time.time()
        result = models.predict(X_test)
        time4= time.time()
        print("pridictTime")
        print(time4-time3)
        listOne = result[0:]  #获取识别图片的所有裁剪结果
        oneResult = analysisType.resultType(listOne)
    return oneResult,"智联招聘"


if __name__ == "__main__":

    #picOpen('../static/image/生活_t.png')
    path = '../static/image/生活_t.png'
    imageHandle = Image.open(path)
    L = imageHandle.convert('L')  # 转化为灰度图
    im_array = np.array(L)
    im = Image.fromarray(im_array.astype('uint8'))  #对图片进行复原
    r=predictBank(im)
    print(r)
#predictBank(im, 'pic2')


