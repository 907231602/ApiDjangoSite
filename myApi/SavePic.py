#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
from myApi.models import SystemPic
import win_unicode_console
win_unicode_console.enable()
import sqlite3


def insertPic(*kw):
    #kw[0]:系统名称；kw[1]:图片名称列表，
    # systemNames=kw[0]
    # SystemPic.objects.filter(systemName=systemNames).delete()
    # for line in kw[1]:
    #     SystemPic.objects.create(systemName=systemNames,picName=line)
        #print(s.systemName,s.picName)
    # SystemPic.objects.filter(systemName='东风').delete()
    # re=SystemPic.objects.all()
    # for t in re:
    #     print(t.picName)

    #插入数据
    systemNames = kw[0]
    conn = sqlite3.connect('E:\\PyCharmWork\\PythonWebApp\\test.db')
    c = conn.cursor()
    print("Opened database successfully")
    for line in kw[1]:
        c.execute("INSERT INTO SystemPic  \
                VALUES (null, "+systemNames+", "+line+")")
    conn.commit()
    print("Records created successfully")
    conn.close()

def getPicInfo(*kw):
    # systemNames = kw[0]
    # conn = sqlite3.connect('E:\\PyCharmWork\\PythonWebApp\\test.db')
    # c = conn.cursor()
    # cursor = c.execute("SELECT picName from SystemPic where systemName='%s'" % systemNames)
    # listName=list()
    # for row in cursor:
    #    listName.append(row[0])
    # conn.close()
    # return  listName
    systemNames = kw[0]
    rs =SystemPic.objects.filter(systemName=systemNames).values('picName')
    listName = list()
    for line in rs:
        listName.append(line['picName'])
    print(listName)
    return listName



