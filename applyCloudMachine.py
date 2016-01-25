__author__ = 'tomchen'
import threading
import subprocess
import sys
import socket
import os
from subprocess import Popen
import time
def prepare():
    if len(sys.argv) != 3:
        print 'usage: python install.py <describe1> <describe2>'
        sys.exit(-1)
    #bash applyfinal.sh my linux 10 Test_01
    subprocess.call('dos2unix *.sh',shell=True)
    subprocess.call('dos2unix *.csh',shell=True)
    global ip1,ip2,host1, host2, masterPath
    global asePort1,asePort2,sidDowncase,sidUppercase,instanceNum,winIp
    des1=sys.argv[1]
    des2=sys.argv[2]
    project='my'
    platform='linux'
    volSize='10'
    print 'apply for ' + des1 + ' is running...'
    print 'apply for ' + des2 + ' is running...'
    p1=Popen(['bash', 'applyfinal.sh',  project, platform, volSize,des1])
    p2=Popen(['bash', 'applyfinal.sh',  project, platform, volSize,des2])
    p1.communicate()
    p2.communicate()
    if os.path.isdir(des1):
        filename= des1+'.info'
        if os.path.exists(filename):
            message = 'OK, the "%s" file exists.'
            print message  % filename
            returnFile = open(filename)
            global  host1
            host1=returnFile.readline().strip('\n')
            print 'Ok,get host1' + host1
            returnFile.close()
    else:
        message = 'Error, the "%s" folder  not exists.'
        print message  % des1

    if os.path.isdir(des2):
        filename= des2 + '/'+des2+'.info'
        if os.path.exists(filename):
            message = 'OK, the "%s" file exists.'
            print message  % filename
            returnFile = open(filename)
            global  host2
            host2=returnFile.readline().strip('\n')
            print 'Ok,get host2' + host2
            returnFile.close()
    else:
        message = 'Error, the "%s" folder  not exists.'
        print message  % des1
    subprocess.call('rm -rf ' + des1 + ' ' + des2,shell=True)
    ip1 = socket.gethostbyname(host1)
    ip2 = socket.gethostbyname(host2)
    print '==========ip1 '+ ip1 +' =========='
    print '==========ip2 '+ ip2 +' =========='
    sidDowncase = 'pi1'
    sidUppercase = 'PI1'
    asePort1 = '****'
    asePort2 = '****'
    instanceNum = '**'
    winIp = '10.173.**.***'
    masterPath='/hadr/packages/master_702'
    print '==========init variables end=========='

prepare()
