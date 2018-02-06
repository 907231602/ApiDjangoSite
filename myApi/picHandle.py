#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
import math
import os
import random
from myApi.SavePic import insertPic
from . import ScreenExpansion as screen
#灰度处理,并转化成数组
def imageHanle(imgName):
    imageHandle = Image.open(imgName)
    L= imageHandle.convert('L')   #转化为灰度图
    im_array = np.array(L)
    return im_array


def cropPic200_200():
    im=Image.open("static/image/tt.png")
    im_size = im.size
    print("图片信息：", im_size)
    numX = im_size[0] / 200
    numY = im_size[1] / 200
    # 第1块           个数
    w = im_size[0] / numX  # 设置被切长度  13.66/2 的倍数
    h = im_size[1] / numY  # 设置被切宽度  7.28/2的倍数
    print(w, h)
    x = 0  # 长
    y = 0  # 宽
    for i in range(math.ceil(numY)):  # 循环宽度4次
        for j in range(math.ceil(numX)):  # 循环长度7次
            region = im.crop((x, y, x + w, y + h))
            region.save("static/imageCrop/crop_average2-%d-%d.png" % ( i, j))
            x = x + w
            y = y
        x = 0  # 高依次增加，宽度从0~~边界值
        y = y + h

#将图片分解成数组，从本地保存的图片加载
def PredictDataHandle(im):
    cropPic200_200()
    X = list()
    Y = list()
    files = os.listdir('static/imageCrop')
    for item in files:
        ele = item.split('e')
        picCat = ele[2].split('-')[0]
        X.append(imageHanle('static/imageCrop/' + item))
        Y.append(picCat)
        # print('Y-->', Y)
    x = np.array(X)
    y = np.array(Y)
    # print('y==>>', y)
    return (x, y)

#获取指定路径下训练图片，把图片切割并转化成数组，把图片对应的one_hot一起返回
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


#传入一张图片，并对图片进行切割，把切割好的图片转化数组加入到list，
def testPredictDataHandle200(im):
    try:
        X = list()
        Y = list()
        im_size = im.size
        #print("图片信息：",im_size)

        numX=im_size[0]/200
        numY=im_size[1]/200
        # 第1块           个数
        w = im_size[0] / numX  # 设置被切长度  13.66/2 的倍数
        h = im_size[1] / numY  # 设置被切宽度  7.28/2的倍数
        #print(w,h)
        x = 0  # 长
        y = 0  # 宽

        for i in range(math.ceil(numY)):  # 循环宽度4次
            for j in range(math.ceil(numX)):  # 循环长度7次
                region = im.crop((x, y, x + w, y + h))
                X.append(np.array(region))      #将图片切割，并把切割好的图片数组保存
                Y.append(1)
                #region.save("static/imageTests/crop_average_8-%d-%d-%d.png" % (k, i, j))
                x = x + w
                y = y
            x = 0  # 高依次增加，宽度从0~~边界值
            y = y + h

        X = np.array(X)
        Y = np.array(Y)

        return (X, Y)
    except BaseException as e:
        print('testPredictDataHandle200 Exception run.............>>>>>>',e)



if __name__ == "__main__":
    #path='../static/image/生活_t.png'
    path='E:/PyCharmWork/CNN_Bank/dataPic/picTrain/js_首页_5.png'
    imageHandle = Image.open(path)
    L = imageHandle.convert('L')  # 转化为灰度图
    L.save('E:/PyCharmWork/PythonWebApp/ApiDjangoSite/static/imageTrain/移动/ss.png')
    #im_array = np.array(L)

    # x , y=trainDataBankHandle200('腾讯','../static/imageTrain/20180110/腾讯')
    # print(x.shape)
    # print(y[0])