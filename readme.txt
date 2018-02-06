图片：（1366*1728），使用前，确保把ZMQ文件内容移动到与ApiDjangoSite(最外层)同级目录
ApiDjangoSite:结合keras+Django,
运行：
启动ZMQ:python ZMQ_Server.py；运行前修改保存路径
       python ZMQ_Work.py
启动Django输入：python manage.py runserver 0.0.0.0:8000

操作：1.先点击注册，进行系统注册，输入系统名，点击完成；
     2.点击截图，进行系统截图，输入图片名称，点击完成；（建议一种类型的页面多截几张）
     3.点击完成，图片数量对比，完成图片库训练
     4.退出：退出系统
     5.最小化：小飞机最小化

ApiDjangoSite:用于配置路径，修改一些参数
demo文件夹：自己写的demo 参考例子

myApi:
    admin.py:未用,必须保留
    apps.py:未用,必须保留
    tests.py:未用,必须保留
    Cnn_train_1920_1080.py:训练图片的方法，（现在舍弃，可不用）
    models.py：存放模型
    picHandle.py：图片处理，图片切割，数组化
    PreDictBankFunc.py：预测图片，返回预测数组
    ResultAnalysis.py：对预测的结果进行分析
    SavePic.py：保存图片种类（类别）到数据库
    ScreenExpansion.py：扩展图片大小到1366*728
    urls.py:访问路径,访问时：ip:8000/myapi/路径
    view.py:处理请求，返回结果

static:静态资源保留地方
       h5:保存训练好的库
       image：测试图片
       imageTrain:保存训练的图片
       ZMQ:暂时保存ZMQ的操作代码
       -----ZMQ_Server.py:消息队列服务器端，负责训练图片
       -----ZMQ_Work.py：消息队列转发
       django.log:未用

b.py:操作sqlite3数据库的代码
db.sqlite3:数据库，现在不用
test.db:数据库，现在用的，保存各个图片类别
error.txt:错误、异常记录

接口.txt: 接口文件