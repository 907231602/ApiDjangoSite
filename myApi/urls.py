#!/usr/bin/env python3.5.2
# -*- coding: utf-8

from . import views
from django.urls import path

urlpatterns = [
    path('analysis/', views.picAnalysis),   #图片分析
    path('save/',views.savePic),            #保存上传数组——》图片
    path('train/',views.trainPic),          #训练图片
    path('ensure/',views.ensurePic),        #核对图片数量，进行训练
    path('insert/',views.insertPics),        #对数据库操作的demo
    path('analysis2/',views.picAnalysis2),
    path('load/',views.filepath),

]