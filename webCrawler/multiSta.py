__author__ = 'admin'
# encoding: UTF-8
#多线程处理程序
import threading
import time,os,sys

#全局变量
SUM = 0
BOY = 0
GIRL = 0
SECRET = 0
UNKOWN = 0

class StaFileList(threading.Thread):
    #文本名称列表
    fileList = []

    def __init__(self, fileList):
        threading.Thread.__init__(self)
        self.fileList = fileList

    def run(self):
        global SUM, BOY, GIRL, SECRET
        if mutex.acquire(1):
            #也可以调用staCorrectFiles函数
            self.staCorrectFiles(self.fileList)
            mutex.release()

    #处理输入的files列表，统计男女人数
    #注意这儿数据同步问题
    #只统计correct开头的列表
    def staCorrectFiles(self, files):
        global SUM, BOY, GIRL, SECRET
        for name in  files:
            newName = 'E:\\pythonProject\\ruisi\\%s' % (name)
            readFile = open(newName,'r')
            for line in readFile:
                sexInfo = line.split()[1]
                SUM +=1
                if sexInfo == u'\u7537' :
                    BOY += 1
                elif sexInfo == u'\u5973':
                    GIRL +=1
                elif sexInfo == u'\u4fdd\u5bc6':
                    SECRET +=1
            # print "thread %s, until %s, total is %s; %s boys; %s girls;" \
            #       " %s secret;" %(self.name, name, SUM, BOY,GIRL,SECRET)
    #处理输入的files列表，统计男女人数
    #注意这儿数据同步问题
    #统计correct、errTime、unkownsex开头的列表
    def staManyFiles(self, files):
        global SUM, BOY, GIRL, SECRET,UNKOWN
        for name in  files:
            if name.startswith('correct') :
                newName = 'E:\\pythonProject\\ruisi\\%s' % (name)
                readFile = open(newName,'r')
                for line in readFile:
                    sexInfo = line.split()[1]
                    SUM +=1
                    if sexInfo == u'\u7537' :
                        BOY += 1
                    elif sexInfo == u'\u5973':
                        GIRL +=1
                    elif sexInfo == u'\u4fdd\u5bc6':
                        SECRET +=1
                # print "thread %s, until %s, total is %s; %s boys; %s girls;" \
                #       " %s secret;" %(self.name, name, SUM, BOY,GIRL,SECRET)
            #没有活动时间，但是有性别
            elif name.startswith("errTime"):
                newName = 'E:\\pythonProject\\ruisi\\%s' % (name)
                readFile = open(newName,'r')
                for line in readFile:
                    sexInfo = line.split()[1]
                    SUM +=1
                    if sexInfo == u'\u7537' :
                        BOY += 1
                    elif sexInfo == u'\u5973':
                        GIRL +=1
                    elif sexInfo == u'\u4fdd\u5bc6':
                        SECRET +=1
                # print "thread %s, until %s, total is %s; %s boys; %s girls;" \
                #       " %s secret;" %(self.name, name, SUM, BOY,GIRL,SECRET)
            #没有性别，也没有时间，直接统计行数
            elif name.startswith("unkownsex"):
                newName = 'E:\\pythonProject\\ruisi\\%s' % (name)
                # count = len(open(newName,'rU').readlines())
                #对于大文件用循环方法，count 初始值为 -1 是为了应对空行的情况，最后+1得到0行
                count = -1
                for count, line in enumerate(open(newName, 'rU')):
                    pass
                count += 1
                UNKOWN += count
                SUM += count
                # print "thread %s, until %s, total is %s; %s unkownsex" %(self.name, name, SUM, UNKOWN)


def test():
    files = []
    #用来保存所有的线程，方便最后主线程等待所以子线程结束
    staThreads = []
    i = 0
    for filename in os.listdir(r'E:\pythonProject\ruisi'):
        #没获取10个文本，就创建一个线程
        if filename.startswith("correct") or filename.startswith("errTime")  or filename.startswith("unkownsex"):
            files.append(filename)
            i+=1
            if i == 20 :
                staThreads.append(StaFileList(files))
                files = []
                i = 0
    #最后剩余的files，很可能长度不足10个
    if files:
        staThreads.append(StaFileList(files))

    for t in staThreads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in staThreads:
        t.join()



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    startTime = time.clock()
    mutex = threading.Lock()
    test()
    print "Multi Thread, total is %s;  %s boys; %s girls; %s secret; %s unkownsex" %(SUM, BOY,GIRL,SECRET,UNKOWN)
    endTime = time.clock()
    print "cost time " + str(endTime - startTime) + " s"
