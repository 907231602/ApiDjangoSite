#!/usr/bin/env python3.5.2
# -*- coding: utf-8 -*-
import sqlite3

#操作数据库，查看数据表内容

#删表
# conn = sqlite3.connect('test.db')
# print("Opened database successfully")
# conn.execute("DROP TABLE SystemPic;")
# conn.commit()
# conn.close()


#建表
# conn = sqlite3.connect('test.db')
# print("Opened database successfully")
# c = conn.cursor()
# c.execute('''CREATE TABLE COMPANY
#        (ID INTEGER PRIMARY KEY    AUTOINCREMENT NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')
# print("Table created successfully")
# conn.commit()
# conn.close()

#插入数据
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# print("Opened database successfully")
# pp='make'
# c.execute("INSERT INTO COMPANY  \
#       VALUES (NULL,'Paul', 32, '"+pp+"', 20000.00 )");

# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (NULL,'Allen', 25, 'Texas', 15000.00 )");
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (NULL,'Teddy', 23, 'Norway', 20000.00 )");
#
# c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (NULL,'Mark', 25, 'Rich-Mond ', 65000.00 )");

# conn.commit()
# print("Records created successfully")
# conn.close()



#查询
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# print("Opened database successfully")
#
# cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print("ID = ",row[0])
#    print("NAME = ", row[1])
#    print("ADDRESS = ", row[2])
#    print("SALARY = ", row[3]), "\n"
#
# print("Operation done successfully")
# conn.close()



#删除
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# print("Opened database successfully")
#
# c.execute("DELETE from COMPANY where ID=2;")
# conn.commit()
# print("Total number of rows deleted :", conn.total_change)
#
# cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3]), "\n"
#
# print ("Operation done successfully")
# conn.close()
#=================操作：conn /django=================================

# def getPic(request):
#     #re = SystemPic.objects.filter(systemName='Paul').values('systemName', 'picName')
#     re = SystemPic.objects.filter().values('systemName', 'picName')
#     print('hello')
#     for t in re:
#         print(t['picName'])
#         print(t['systemName'])
#     return HttpResponse('1')
#
# def insertSqlByDjango(request):
#     SystemPic.objects.create(systemName='隆正',picName='CC')
#     return HttpResponse('1')
#
#
# def insertSql(request):
#     # 插入数据
#     conn = sqlite3.connect('test.db')
#     c = conn.cursor()
#     print("Opened database successfully")
#
#     c.execute("INSERT INTO trainApi_systempic VALUES (null,'Paul','California')")
#
#     conn.commit()
#     print("Records created successfully")
#     conn.close()
#     return HttpResponse('1')
#
#
# #获取数据库表
# def getDB(request):
#     #[('COMPANY',), ('SystemPic',), ('auth_group',), ('auth_group_permissions',), ('auth_permission',),
#     # ('auth_user',), ('auth_user_groups',), ('auth_user_user_permissions',), ('django_admin_log',),
#     # ('django_content_type',), ('django_migrations',), ('django_session',), ('sqlite_sequence',),
#     # ('trainApi_systempic',)]
#
#     conn = sqlite3.connect('test.db')
#     print(conn.execute("select name from sqlite_master where type = 'table' order by name").fetchall())
#     # rs=conn.execute("show tables")
#     # conn.commit()
#     # for line in rs:
#     #     print(line)
#
#     conn.close()
#     return HttpResponse('1')

#================================创建保存图片的数据库=================================================

#删表
# conn = sqlite3.connect('test.db')
# print("Opened database successfully")
# conn.execute("DROP TABLE SystemPic;")
# conn.commit()
# conn.close()

#建表
# conn = sqlite3.connect('test.db')
# print("Opened database successfully")
# c = conn.cursor()
# c.execute('''CREATE TABLE SystemPic
#        (ID INTEGER PRIMARY KEY    AUTOINCREMENT NOT NULL,
#         systemName         CHAR(200)     NOT NULL,
#         picName            CHAR(200)     NOT NULL
#         );''')
# print("Table created successfully")
#     #conn.execute("DROP TABLE COMPANY;")#删除表
# conn.commit()
# conn.close()

#插入数据
conn = sqlite3.connect('test.db')
c = conn.cursor()
print("Opened database successfully")

c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '投资.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '登录.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '生活.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '首页.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '转账.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '资产.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '网银.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '信用卡.png' )");
c.execute("INSERT INTO myapi_systemPic  \
      VALUES (NULL,'建行',  '贷款.png' )");

conn.commit()
print("Records created successfully")
conn.close()


#查询
conn = sqlite3.connect('test.db')
c = conn.cursor()
print("Opened database successfully")

cursor = c.execute("SELECT id,systemName,picName from myapi_systemPic")
for row in cursor:
   print("ID = ",row[0])
   print("NAME = ", row[1])
   print("picName = ", row[2]), "\n"

print("Operation done successfully")
conn.close()


#删除
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
# print("Opened database successfully")
#
# c.execute("DELETE from myapi_systemPic where systemName='建行'")
# conn.commit()
# print("Total number of rows deleted :", conn.total_change)

# cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3]), "\n"
#
# print ("Operation done successfully")
# conn.close()