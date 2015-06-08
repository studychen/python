__author__ = 'I316736'
import threading
import subprocess
import sys
import socket
import os
from subprocess import Popen
import time

def prepare():
    if len(sys.argv) != 3:
        print 'usage: python install.py <host1> <host2>'
        sys.exit(-1)
    subprocess.call('dos2unix *.sh',shell=True)
    subprocess.call('dos2unix *.csh',shell=True)
    global ip1,ip2,host1, host2, masterPath,packages,silent
    global asePort1,asePort2,sidDowncase,sidUppercase,instanceNum,winIp
    host1=sys.argv[1]
    host2=sys.argv[2]
    ip1 = socket.gethostbyname(host1)
    ip2 = socket.gethostbyname(host2)
    print '==========ip1 '+ ip1 +' =========='
    print '==========ip2 '+ ip2 +' =========='
    sidDowncase = 'pi1'
    sidUppercase = 'PI1'
    asePort1 = '4901'
    asePort2 = '4901'
    instanceNum = '00'
    masterPath='/hadr/packages/master'
    packages='/hadr/sumAuto/autoInstall/packages'
    silent='/hadr/sumAuto/packages/silentInstall'
    print '==========init variables end=========='


def copyPackages(ip):
    print '==========copy silentInstall on ' + ip + ' running ...    =========='
    subprocess.call('./pscp -q -r -pw Sybase123 '+ silent+ ' root@'+ip+':/hadr' , shell=True)
    print '==========copy silentInstall on ' + ip + ' succeed  =========='

    print '==========copy packages on ' + ip + ' running ... please wait ... =========='
    subprocess.call('./pscp -q -r -pw Sybase123 ' +packages+ ' root@'+ip+':/hadr', shell=True)
    print '==========copy packages on ' + ip + ' succeed       =========='


def priAse():
    copyPackages(ip1)
    priAseF=open('priAse', 'w')
    print '========== primary ASE installation running ...    =========='
    result = subprocess.call("java -jar ./exeRemoteCmd.jar "+ip1+' \" cd /hadr/silentInstall && /bin/bash /hadr/silentInstall/run.sh NW741 ' + masterPath + ' ' + host1+' ' +host2+ '\"', shell=True,stdout=priAseF)
    if result != 0:
        print 'install primary ase error'
        sys.exit(-1)
    priAseF.close()
    print '========== primary ASE succeed    =========='

def staAse():
    copyPackages(ip2)
    staAseF=open('staAse', 'w')
    print '========== standby ASE installation running ...   =========='
    result = subprocess.call("java -jar ./exeRemoteCmd.jar " +ip2+ ' \" cd /hadr/silentInstall && /bin/bash /hadr/silentInstall/run.sh NW741_SYSCOPY ' + masterPath + ' ' + host1+' ' +host2+ '\"', shell=True,stdout=staAseF)
    if result != 0:
        print 'install standby ase error'
        sys.exit(-1)
    staAseF.close()
    print '========== standby ASE succeed    =========='

def staAseRs():
    thread = threading.Thread(target=staAse)
    thread.start()
    thread.join()
    print '========== standby RS installation running ...    =========='
    staRsF=open('staRs', 'w')
    result = subprocess.call("java -jar ./exeRemoteCmd.jar " +ip2+ ' \" cd /hadr/silentInstall && /bin/bash /hadr/silentInstall/run.sh NW741_RS_STANDBY ' + masterPath + ' ' + host1+' ' +host2+ '\"', shell=True,stdout=staRsF)
    if result != 0:
        print 'install standby rs error'
        sys.exit(-1)
    staRsF.close()
    print '========== standby RS succeed    =========='

def priRs():
    priRsF=open('priRs', 'w')
    print '========== primary RS installation running ...    =========='
    result = subprocess.call("java -jar ./exeRemoteCmd.jar "+ip1+' \" cd /hadr/silentInstall && /bin/bash /hadr/silentInstall/run.sh NW741_RS_PRIMARY ' + masterPath + ' ' + host1+' ' +host2+ '\"', shell=True,stdout=priRsF)
    if result != 0:
        print 'install primary rs error'
        sys.exit(-1)
    priRsF.close()
    print '========== primary RS succeed    =========='

def checkSilentSuccess(ip):
    print '==========   will check  Hadr env       =========='
    portArray=['4901','4902','4903','4905','4906','4907','4907','4909']
    for port in portArray:
        result = subprocess.call('./plink -pw Sybase123 root@'+ ip + ' netstat -tnpl | grep ' + port + ' > /dev/null', shell=True)
        if result != 0:
            print port + ' in ' + ip +' not listen'
            sys.exit(-1)
        else:
             print port + ' in ' + ip +' listen'
    print '========== OK, '+ ip+ ' Hadr env is OK    =========='

def installHadr():
    threadPriAse = threading.Thread(target=priAse)
    threadPriAse.start()
    time.sleep(1)
    threadStaAseRs = threading.Thread(target=staAseRs)
    threadStaAseRs.start()
    threadPriAse.join()
    threadStaAseRs.join()
    priRs()
    print '========== install Hadr succeed  =========='

def checkHadrSuccess():
    checkSilentSuccess(ip1)
    checkSilentSuccess(ip2)

def main():
    prepare()
    installHadr()
    checkHadrSuccess()

main()


