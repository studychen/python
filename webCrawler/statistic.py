# encoding: UTF-8
#统计数据，这儿都是单线程
import os,time,threading,sys
reload(sys)
sys.setdefaultencoding('utf-8')


def staUnkownsex():
    startTime = time.clock()
    unkownCount = 0
    for filename in os.listdir(r'E:\pythonProject\ruisi'):
        if filename.startswith('unkownsex'):
            count = 0
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            readFile = open(newName,'r')
            for line in readFile:
                count += 1
                unkownCount +=1
            print "%s deal %s lines" %(filename, count)
    print '%s unkowns sex' %(unkownCount)
    endTime = time.clock()
    print "cost time " + str(endTime - startTime) + " s"


def staCorrect():
    startTime = time.clock()
    sumCount = 0
    boycount = 0
    girlcount = 0
    secretcount = 0
    for filename in os.listdir(r'E:\pythonProject\ruisi'):
        if filename.startswith('correct'):
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            readFile = open(newName,'r')
            for line in readFile:
                sexInfo = line.split()[1]
                sumCount +=1
                if sexInfo == u'\u7537' :
                    boycount += 1
                elif sexInfo == u'\u5973':
                    girlcount +=1
                elif sexInfo == u'\u4fdd\u5bc6':
                    secretcount +=1
            # print "until %s, sum is %s boys; %s girls; %s secret;" %(filename, boycount,girlcount,secretcount)
    print "Single Thread, total is %s;  %s boys; %s girls; %s secret;" %(sumCount, boycount,girlcount,secretcount)
    endTime = time.clock()
    print "cost time " + str(endTime - startTime) + " s"

def staManyKinds():
    startTime = time.clock()
    sumCount = 0
    boycount = 0
    girlcount = 0
    secretcount = 0
    unkowncount = 0
    for filename in os.listdir(r'E:\pythonProject\ruisi'):
        # 有性别、活动时间
        if filename.startswith('correct') :
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            readFile = open(newName,'r')
            for line in readFile:
                sexInfo =line.split()[1]
                sumCount +=1
                if sexInfo == u'\u7537' :
                    boycount += 1
                elif sexInfo == u'\u5973':
                    girlcount +=1
                elif sexInfo == u'\u4fdd\u5bc6':
                    secretcount +=1
            # print "until %s, sum is %s boys; %s girls; %s secret;" %(filename, boycount,girlcount,secretcount)
        #没有活动时间，但是有性别
        elif filename.startswith("errTime"):
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            readFile = open(newName,'r')
            for line in readFile:
                sexInfo =line.split()[1]
                sumCount +=1
                if sexInfo == u'\u7537' :
                    boycount += 1
                elif sexInfo == u'\u5973':
                    girlcount +=1
                elif sexInfo == u'\u4fdd\u5bc6':
                    secretcount +=1
            # print "until %s, sum is %s boys; %s girls; %s secret;" %(filename, boycount,girlcount,secretcount)
        #没有性别，也没有时间，直接统计行数
        elif filename.startswith("unkownsex"):
            newName = 'E:\\pythonProject\\ruisi\\%s' % (filename)
            # count = len(open(newName,'rU').readlines())
            #对于大文件用循环方法，count 初始值为 -1 是为了应对空行的情况，最后+1得到0行
            count = -1
            for count, line in enumerate(open(newName, 'rU')):
                pass
            count += 1
            unkowncount += count
            sumCount += count
            # print "until %s, sum is %s unkownsex" %(filename, unkowncount)

    print "Single Thread, total is %s;  %s boys; %s girls; %s secret; %s unkownsex;" %(sumCount, boycount,girlcount,secretcount,unkowncount)
    endTime = time.clock()
    print "cost time " + str(endTime - startTime) + " s"

staCorrect()