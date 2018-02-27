#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
from django.http import JsonResponse,HttpRequest
import sqlite3
from myApi.PreDictBankFunc import predictBank
from myApi.models import Pic
import simplejson
from django.core.serializers import serialize
#from django.test import override_settings
import numpy as np
from PIL import Image
import io
import os
from . import Cnn_train_1920_1080 as bankTrain
from . import ScreenExpansion as screen
#from myApi.models import SystemPic
import threading
from myApi.SavePic import getPicInfo
import zmq
import win_unicode_console
win_unicode_console.enable()
import socket
import  base64
# Create your views here.

#图片分类、识别,返回json类型的图片数据
#@override_settings(DATA_UPLOAD_MAX_MEMORY_SIZE=10242880)
def picAnalysis(request):
    try:
        req = simplejson.loads(request.body)
        Image.frombytes()

        # 对图片进行处理，把传过来的数组进行还原
        listpic = req['KeyWord']

        #还原图片
        shapePic = np.array(listpic).shape
        print('===>数组大小：', shapePic[0], shapePic[1])
        ar = np.array(listpic).reshape(shapePic[0], shapePic[1])
        ar = ar.T  # 倒置,目的是把图片还原
        im = Image.fromarray(ar.astype('uint8'))

        #修改屏幕大小
        #im=screen.ScreenExpans(im)
        #im=screen.ScreenExpansResize(im)
        im=screen.ScreenExpansCommon(im)
        #im.save('static/image/hello.png')

        prenum,systemTypeName=predictBank(im)  #对图片进行预测，并返回预测结果
        im.close()

        pic = Pic()
        pic.picName = '哈哈'
        pic.picNumType = prenum
        if (prenum == 0):
            pic.picTypeName='未知页面'
        else:
            listSys = getPicInfo(systemTypeName)
            pic.picTypeName = listSys[prenum - 1]
        d = simplejson.loads(serialize('json', [pic])[1:-1])
        return JsonResponse(d)
    except ConnectionResetError as ce:
        print("远程主机强迫关闭了一个现有的连接",ce)
        return JsonResponse({'info':'error'})

    except ConnectionAbortedError as er:
        print('er:',er)
    except socket.timeout as e:
        print("-----socket timout:", e)

def picAnalysisBase64(request):
    try:
        print(request.META['CONTENT_LENGTH'])
        req = simplejson.loads(request.body)
        
        # 对图片进行处理，把传过来的数组进行还原
        basePic = req['PicBase64']

        # 还原图片信息
        imgdata = base64.b64decode('''%s''' % basePic)
        stream = io.BytesIO(imgdata)
        im = Image.open(stream)
        im = im.convert('L')  # 灰度
        # 修改屏幕大小
        im = screen.ScreenExpansCommon(im)

        prenum, systemTypeName = predictBank(im)  # 对图片进行预测，并返回预测结果
        im.close()

        pic = Pic()
        pic.picName = '哈哈'
        pic.picNumType = prenum
        if (prenum == 0):
            pic.picTypeName = '未知页面'
        else:
            listSys = getPicInfo(systemTypeName)
            pic.picTypeName = listSys[prenum - 1]
        d = simplejson.loads(serialize('json', [pic])[1:-1])
        return JsonResponse(d)
    except ConnectionResetError as ce:
        print("远程主机强迫关闭了一个现有的连接", ce)
        return JsonResponse({'info': 'error'})

    except ConnectionAbortedError as er:
        print('er:', er)
    except socket.timeout as e:
        print("-----socket timout:", e)


    #分析图片2,用于测试，不实用
def picAnalysis2(request):
    try:
        print('hello')
        im=Image.open('static/imageTrain/建行/20180119164616_投资.png')
        prenum, systemTypeName = predictBank(im)  # 对图片进行预测，并返回预测结果
        im.close()

        pic = Pic()
        pic.picName = '哈哈'
        pic.picNumType = prenum
        if (prenum == 0):
            pic.picTypeName = '未知页面'
        else:
            listSys = getPicInfo(systemTypeName)
            pic.picTypeName = listSys[prenum - 1]
        d = simplejson.loads(serialize('json', [pic])[1:-1])
        return JsonResponse(d)
    except ConnectionError as ce:
        print('异常',ce)
        return JsonResponse({"info":"2"})


#保存图片，以日期(天)为单位，在日期文件下判断类别是否存在，否就创建，在类别下保留图片.  日期->类别->图片
#@override_settings(DATA_UPLOAD_MAX_MEMORY_SIZE=10242880)
def savePic(request):
    try:
        basepath='static/imageTrain'
        req = simplejson.loads(request.body)
        name = str(req['Name']).split('_')  #name[0]：系统名；name[1]:时间；name[2]:图片名称
        print('name=',name)
        if (name == "" or name == None):
            return JsonResponse({'info': '系统名为空'})
        # 对图片进行处理，把传过来的数组进行还原
        listpic = req['KeyWord']
        #还原图片信息
        shapePic=np.array(listpic).shape
        print('===>数组大小：',shapePic[0], shapePic[1])
        ar = np.array(listpic).reshape(shapePic[0],shapePic[1])
        ar = ar.T  # 倒置,目的是把图片还原
        im = Image.fromarray(ar.astype('uint8'))

        # 修改屏幕大小
        #im=screen.ScreenExpans(im)
        #im=screen.ScreenExpansResize(im)
        im = screen.ScreenExpansCommon(im)

        #确定文件夹,系统文件夹存在则保留图片，不存在则新建
        #now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')#当前时间
        is_exit=os.path.exists(basepath+'/%s' % name[0])
        if(is_exit):
            pass
        else:
            os.makedirs(basepath+'/%s' % name[0])
        im.save(basepath+'/%s/%s_%s.png' % (name[0],name[1],name[2]))
        im.close()
        return JsonResponse({'info':'Ok'})
    except BaseException as e:
        print('e===',e)
        return JsonResponse({'info': 'error'})


def savePicBase64(request):
    try:
        basepath = 'static/imageTrain'
        req = simplejson.loads(request.body)
        name = str(req['Name']).split('_')  # name[0]：系统名；name[1]:时间；name[2]:图片名称
        print('name=', name)
        if (name == "" or name == None):
            return JsonResponse({'info': '系统名为空'})
        # 对图片进行处理，把传过来的数组进行还原
        basePic = req['PicBase64']
        # 还原图片信息
        imgdata = base64.b64decode('''%s''' % basePic)
        stream = io.BytesIO(imgdata)
        im = Image.open(stream)
        im = im.convert('L')  #灰度
        # 修改屏幕大小
        im = screen.ScreenExpansCommon(im)

        # 确定文件夹,系统文件夹存在则保留图片，不存在则新建
        # now=datetime.datetime.now().strftime('%Y%m%d%H%M%S')#当前时间
        is_exit = os.path.exists(basepath + '/%s' % name[0])
        if (is_exit):
            pass
        else:
            os.makedirs(basepath + '/%s' % name[0])
        # file = open(basepath + '/%s/%s_%s.png' % (name[0], name[1], name[2]), 'wb')
        # file.write(imgdata)
        # file.close()
        # im=Image.open(basepath + '/%s/%s_%s.png' % (name[0], name[1], name[2]))
        # im=im.convert('L')
        # im = screen.ScreenExpansCommon(im)#大小转化
        im.save(basepath + '/%s/%s_%s.png' % (name[0], name[1], name[2]))
        # im.save(basepath + '/%s/%s_%s.png' % (name[0], name[1], name[2]))
        im.close()
        return JsonResponse({'info': 'Ok'})
    except BaseException as e:
        print('e===', e)
        return JsonResponse({'info': 'error'})



#确认上传图片是否丢失
def ensurePic(request):
    #根据系统名称确定图片是否有没上传上来的（确认是否丢失）,
    try:
        req = simplejson.loads(request.body)
        name = req['Name']  #系统名称
        if(name=="" or name==None):
            return JsonResponse({'info':'系统名为空'})
        picNum=req['Num']   #上传过来的图片数量
        #先确定图片是否已经训练过，用后缀“_"判断，
        basePath = 'static/imageTrain'
        listFile = os.listdir(basePath)
        # 以‘_’结尾的标记已经训练过的图片，标记并判断，如果以“_”结尾，则不处理
        for linefile in listFile:
            if linefile.endswith('_'):
                if (linefile == name+'_'):
                    return JsonResponse({'info':'0'})   #判断图片是否已经训练，已经训练完成返回0
                continue
            else:
                if (linefile == name): #检查系统名是否训练过，没有训练则检查数目是否正确
                    listDirs=os.listdir('static/imageTrain/%s' % name)
                    if(picNum==listDirs.__len__()):
                        #开启训练线程
                        t1 = threading.Thread(target=postTrain,args=(name,))
                        t1.setDaemon(True)
                        t1.start()
                        return JsonResponse({'info':'1'}) #表示图片没有丢失,图片正在训练
                    else:
                         listFileName=list()
                         for line in listDirs:
                             listFileName.append(line)
                         return JsonResponse({'info':listFileName})  #返回图片列表
                else:
                    continue
        return JsonResponse({'info':'-1'}) #不存在该系统
    except BaseException as e:
        print('ensurePic Exception',e)
        return JsonResponse({'info':'error'})

#发送请求到另一项目训练
def postTrain(sysName):

    #参考：http://blog.csdn.net/qq_878799579/article/details/73956344
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind('tcp://*:5557')

    socket.send(sysName.encode('utf-8'))



    #sendDictParams = {'name': sysName}
    #requests.get('http://192.168.6.238:8001/train/trains/', params=sendDictParams)


#图片训练,根据不同系统，训练成不同系统的库，并标记已经训练的库
def trainPic(sysName): #系统名称
    try:
        basePath = 'static/imageTrain'
        bankTrain.Cnn_run(sysName)  # 系统名称
        os.renames(basePath + '/%s' % sysName, basePath + '/%s%s' % (sysName, '_'))
    except BaseException as e:
        print('TrainPic Exception ',e)

    # print('I am start')
    # basePath='static/imageTrain'
    # listFile = os.listdir(basePath)
    # #以‘_’结尾的标记已经训练过的图片，标记并判断，如果以“_”结尾，则不处理
    # for linefile in listFile:
    #     if linefile.endswith('_'):
    #         continue
    #     else:
    #         if(basePath.split('/')[-1]==sysName):
    #             bankTrain.Cnn_run(linefile) #系统名称
    #             #标记训练完成，传入2个传输，原名称、修改名称
    #             os.renames(basePath+'/%s' % linefile,basePath+'/%s%s' % (linefile,'_'))
    #         else:
    #             continue
    # return JsonResponse({'num':listFile.__len__()})


def insertPics(request):

    conn = sqlite3.connect('E:\\PyCharmWork\\PythonWebApp\\test.db')
    c = conn.cursor()
    print("Opened database successfully")

    cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
        print("ID = ", row[0])
        print("NAME = ", row[1])
        print("ADDRESS = ", row[2])
        print("SALARY = ", row[3]), "\n"

    print("Operation done successfully")
    conn.close()
    return JsonResponse({'info':'1'})
    # s=SystemPic()
    # s.systemName='东风'
    # l=['首页','登录','注册','退出','查询','退出']
    # for line in l:
    #     s.picName=line
    #     SystemPic.objects.create(systemName='东风',picName=line)
    # SystemPic.objects.filter(systemName='东风').delete()
    # re=SystemPic.objects.filter(systemName='移动').values('systemName','picName')
    # for t in re:
    #     print(t['picName'])
    # re = SystemPic.objects.filter(systemName='腾讯').values('systemName', 'picName')
    # for t in re:
    #     print(t['picName'])    #from myApi.models import SystemPic

    # SystemPic.objects.filter(systemName='移动').delete()
    # SystemPic.objects.filter(systemName='腾讯').delete()
    # re = SystemPic.objects.filter(systemName='移动').values('systemName', 'picName')
    # for t in re:
    #     print(t['picName'])
    # return JsonResponse({'info':1})


'''
b'Content-Disposition: form-data; name="file";filename="20180110160317_\xe7\x99\xbb\xe5\xbd\x95.png"\r\nContent-Type:application/octet-stream\
r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x02\x00\x00\x00\x04\x08\x00\x00\x00\x00\x81\x84\xb1\xe5\x00\x00\x00\x14IDATx\x9cc0\xff\
xcf\xf8\x9f\x81\x89a\x0e\xc3\x89\xff\x00\x19k\x04\x9c\xe0\xd4\x96&\x00\x00\x00\x00IEND\xaeB`\x82'
'''


# Quit the server with CTRL-BREAK.
# hello
# 186072(Base64)
# [08/Feb/2018 14:05:25] "POST /myapi/load/ HTTP/1.1" 200 16
# hello
# 533143(IO)
# [08/Feb/2018 14:09:05] "POST /myapi/load/ HTTP/1.1" 200 16


def filepath(request):
    print("hello")
    print(request.body)
    print(request.META['CONTENT_LENGTH'])
    req = simplejson.loads(request.body)
    print(req['name'])
    # req = simplejson.loads(request.body)
    # print(req)
    # name=req['Name']
    # print(name)

    #basePic=req['PicBase64']

    # basePic = '''/9j/4AAQSkZJRgABAQEAYABgAAD/4QA6RXhpZgAATU0AKgAAAAgAA1EQAAEAAAABAQAAAFERAAQAAAABAAAAAFESAAQAAAABAAAAAAAAAAD/2wB
    # DAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyM
    # jIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAEAAIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQ
    # RBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp
    # 6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAE
    # CAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmao
    # qOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD220sn+xweTezW8XlrshhjiCRjHCqNnAHQUUUUAf/Z'}'''

    # imgdata = base64.b64decode('''%s''' % basePic)
    # file = open('1.png', 'wb')
    # file.write(imgdata)
    # file.close()

    return JsonResponse({"info":"1111"})



if __name__=='__main__':
    filepath()