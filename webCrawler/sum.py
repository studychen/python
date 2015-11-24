# coding=utf-8
#多线程爬取用户id、性别、活动时间
#调用了ruisi.py
from subprocess import Popen
import subprocess
import threading,time


startn = 1
endn = 300001
step =1000
total = (endn - startn + 1 ) /step
ISOTIMEFORMAT='%Y-%m-%d %X'

#hardcode 3 threads
#沒有深究3个线程好还是4或者更多个线程好
#输出格式化的年月日时分秒
#输出程序的耗时（以秒为单位）
for i in xrange(0,total,3):
    startNumber = startn + step * i
    startTime = time.clock()

    s0 = startNumber
    s1 = startNumber + step
    s2 = startNumber + step*2
    s3 = startNumber + step*3



    p1=Popen(['python', 'ruisi.py', str(s0),str(s1)],bufsize=10000, stdout=subprocess.PIPE)

    p2=Popen(['python', 'ruisi.py', str(s1),str(s2)],bufsize=10000, stdout=subprocess.PIPE)

    p3=Popen(['python', 'ruisi.py', str(s2),str(s3)],bufsize=10000, stdout=subprocess.PIPE)

    startftime ='[ '+ time.strftime( ISOTIMEFORMAT, time.localtime() ) + ' ] '

    print  startftime + '%s - %s download start... ' %(s0, s1)
    print  startftime + '%s - %s download start... ' %(s1, s2)
    print  startftime + '%s - %s download start... ' %(s2, s3)

    p1.communicate()
    p2.communicate()
    p3.communicate()

    endftime = '[ '+ time.strftime( ISOTIMEFORMAT, time.localtime() ) + ' ] '
    print endftime + '%s - %s download end !!! ' %(s0, s1)
    print endftime + '%s - %s download end !!! ' %(s1, s2)
    print endftime + '%s - %s download end !!! ' %(s2, s3)

    endTime = time.clock()
    print "cost time " + str(endTime - startTime) + " s"
    time.sleep(5)



