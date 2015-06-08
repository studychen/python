__author__ = 'I316736'
import threading
import subprocess
import sys
import socket
import os
from subprocess import Popen
import time

def prepare():
    if len(sys.argv) != 6:
        print 'usage: python install.py <pri_ip> <sta_ip> <sid> <ase_port> <fun_name>'
        sys.exit(-1)
    global ip1,ip2,sumAutoLoca
    global asePort1,asePort2,sidDowncase,sidUppercase,pscpLoca,fun_name,remoteCmdLoca,remoteSSHLoca
    ip1=sys.argv[1] #10.173.**.**
    ip2=sys.argv[2]
    sid = sys.argv[3]
    sidDowncase = sid.lower()  #pi1
    sidUppercase = sid.upper() #PI1
    asePort1 = sys.argv[4] #4901
    asePort2 = sys.argv[4]
    fun_name = sys.argv[5]
    pscpLoca = '/hadr/svncopy/10.173.3.23/monitor/sumPreAuto/pscp'
    sumAutoLoca = '/hadr/svncopy/10.173.3.23/monitor/sumPreAuto/'
    remoteCmdLoca = '/hadr/svncopy/10.173.3.23/monitor/exeRemoteCmd.jar' # root
    remoteSSHLoca = '/hadr/svncopy/10.173.3.23/monitor/runRemoteSSHCmd.jar' # user passwd ip
    print ip1.center(30,'=')
    print ip2.center(30,'=')
    print '==========init variables end=========='

def getHostName(ip):
    command = 'java -jar %s %s "hostname > %s.hostname"' %(remoteCmdLoca,ip,ip)
    result = subprocess.call(command, shell=True)
    command = '%s -q -r -pw Sybase123 %s root@%s:/root' % (pscpLoca, pscpLoca, ip)
    result = subprocess.call(command, shell=True)
    command = '%s -q -r -pw Sybase123 root@%s:/root/%s.hostname %s' %(pscpLoca,ip,ip,sumAutoLoca)
    result = subprocess.call(command, shell=True)
    fileName = sumAutoLoca + ip + '.hostname'
    readFile = open(fileName,'r')
    hostnameInfo =  str(readFile.readline().strip('\n'))
    subprocess.call('rm '+ fileName, shell=True)
    print "=========%s hostname is %s========" %(ip,hostnameInfo)
    return hostnameInfo

def checkHadrSuccess():
    def checkInstallSuccess(ip):
        print '==========   will check  Hadr env       =========='
        portArray=['4901','4902','4903','4905','4906','4907','4908','4909']
        for port in portArray:
            command = 'java -jar %s %s "netstat -tnpl | grep %s > /dev/null"' %(remoteCmdLoca,ip,port)
            result = subprocess.call(command, shell=True)
            if result != 0:
                print port + ' in ' + ip +' not listen'
                sys.exit(-1)
            else:
                print port + ' in ' + ip +' listen'
        print '========== OK, '+ ip+ ' Hadr env is OK    =========='
    checkInstallSuccess(ip1)
    checkInstallSuccess(ip2)

def sum_init_cp_Dual_702SP9to702SP12():
    host1 = getHostName(ip1)
    host2 = getHostName(ip2)
    print '=================sum_init_hadrenv running ... =================='
    subprocess.call(pscpLoca + ' -pw Sybase123 ./sumPreAuto/adm_env_init.csh ' + sidDowncase + 'adm@'+ ip1+ ':/home/' + sidDowncase + 'adm',shell=True)
    command = 'java -jar %s %s Sybase123 %s "source /home/%s/adm_env_init.csh %s %s %s"' %(remoteSSHLoca,sidDowncase+'adm',ip1,sidDowncase+'adm',sidUppercase,host1,host2)
    subprocess.call(command,shell=True)
    subprocess.call(pscpLoca + ' -q -pw Sybase123 ./sumPreAuto/alias.sh root@'+ ip1+ ':/root' ,shell=True)
    subprocess.call(pscpLoca + ' -q -pw Sybase123 ./sumPreAuto/alias.sh root@'+ ip2+ ':/root' ,shell=True)
    command = 'java -jar %s %s "source /root/alias.sh %s"' %(remoteCmdLoca,ip1,sidUppercase)
    subprocess.call(command ,shell=True)
    command = 'java -jar %s %s "source /root/alias.sh %s"' %(remoteCmdLoca,ip2,sidUppercase)
    subprocess.call(command ,shell=True)
    print '=================sum_init_hadrenv succeed =================='
    sum_copy_Dual_702SP9to702SP12(ip1,host1)

def sum_copy_Dual_702SP9to702SP12(ip,host):
    print '==========copy Dual_702SP9to702SP12 on ' + ip + ' running ... please wait... =========='
    packLoca = '/hadr/packages/SUMtest/SUMfiles/Dual_702SP9to702SP12'
    command = '%s -q -r -pw Sybase123 %s root@%s:/hadr/' %(pscpLoca,packLoca,ip)
    subprocess.call(command, shell=True)
    print '==========copy Dual_702SP9to702SP12 on ' + ip + ' succeed       =========='
    xmlFile = '/hadr/Dual_702SP9to702SP12/AutoSum_stack_PI1_SUM.xml'
    priVmCommand = 'sed -i "s/SUM_HOST_NAME_NEED_REP/' + host + '/g" ' + xmlFile
    command = 'java -jar %s %s "%s"' %(remoteCmdLoca,ip,priVmCommand)
    result = subprocess.call(command,shell=True)
    print '==========produce AA_stack_PI1_SUM.xml ' + ip + ' succeed    =========='

def installSapcar(ip):
    print '=================installSapcar running ... =================='
    subprocess.call(pscpLoca + ' -pw Sybase123 ./sumPreAuto/installSapcar.sh root@'+ ip + ':/root',shell=True)
    command = 'java -jar %s %s "bash /root/installSapcar.sh"' %(remoteCmdLoca,ip)
    result = subprocess.call(command,shell=True)
    if result != 0:
        print 'installSapcar error'
        sys.exit(-1)
    print '=================installSapcar succeed =================='

def sum_sapcar_SUM10SP12_0_KD70254_STARTUP4239():
    installSapcar(ip1)
    print '=================sumCopyFiles & sapcar files running ... =================='
    suLoca = '/hadr/packages/SUMtest/SUMfiles/SUM10SP12_0.SAR'
    kdLoca = '/hadr/packages/SUMtest/SUMfiles/KD70254.SAR'
    command = '%s -r -pw Sybase123 %s root@%s:/usr/sap/%s/' %(pscpLoca,suLoca,ip1,sidUppercase)
    subprocess.call(command,shell=True)
    command = '%s -r -pw Sybase123 %s root@%s:/usr/sap/trans/' %(pscpLoca,kdLoca,ip1)
    subprocess.call(command,shell=True)
    command = 'java -jar %s %s Sybase123 %s "cd /usr/sap/%s/ && sapcar -xvf SUM10SP12_0.SAR > /dev/null"' %(remoteSSHLoca,sidDowncase+'adm',ip1,sidUppercase)
    subprocess.call(command,shell=True)
    print "==========sapcar SUM10SP12_0.SAR succeed=========="
    command = 'java -jar %s %s Sybase123 %s "cd /usr/sap/trans/ && sapcar -xvf KD70254.SAR > /dev/null"' %(remoteSSHLoca,sidDowncase+'adm',ip1)
    subprocess.call(command,shell=True)
    print "==========  sapcar KD70254.SAR succeed =========="
    command = 'java -jar %s %s Sybase123 %s "cp /usr/sap/%s/SUM/abap/bin/sybctrl /usr/sap/%s/SUM/abap/exe"' %(remoteSSHLoca,sidDowncase+'adm',ip1,sidUppercase,sidUppercase)
    subprocess.call(command,shell=True)
    print "==========  cp /usr/sap/ " + sidUppercase + "/SUM/abap/bin/sybctrl  succeed =========="
    print '=================sumCopyFiles & sapcar files & cp sybctrl succeed   =================='
    sum_startup_4239()

def sum_startup_4239():
    print '================= sum port 4239  starting ... =================='
    sumLocation = '/usr/sap/' + sidUppercase + '/SUM/STARTUP'
    stCommand = 'nohup ' + sumLocation + ' >& /dev/null < /dev/null &'
    command = 'java -jar %s %s Sybase123 %s "%s"' %(remoteSSHLoca,sidDowncase+'adm',ip1,stCommand)
    subprocess.call(command,shell=True)
    port='4239'
    time.sleep(20)
    print '================= check port 4239  listen =================='
    command = 'java -jar %s %s "netstat -tnpl | grep %s"' %(remoteCmdLoca,ip1,port)
    result = subprocess.call(command, shell=True)
    if result != 0:
        print port + ' in ' + ip1 +' not listen'
        sys.exit(-1)
    else:
         print port + ' in ' + ip1 +' listen'
    print '================= sum port 4239  succeed =================='
    # subprocess.call('java -jar  runRemoteWin.jar "cd C:\sumScripts && python sumSapgui ' + ip1 + ' ' + sidUppercase + ' ' + instanceNum +'"' ,shell=True)

def sum_extend_ase_pri_sta():
    print '=================extendTwoAse running ...,please wait... =================='
    p1=Popen(['java', '-jar', './sumPreAuto/extendAse.jar', ip1, asePort1, sidUppercase])
    p2=Popen(['java', '-jar', './sumPreAuto/extendAse.jar', ip2, asePort2, sidUppercase])
    p1.communicate()
    p2.communicate()
    print '=================extendTwoAse '+ ip1+ ' succeed  =================='
    print '=================extendTwoAse '+ ip2+ ' succeed =================='

def main():
    prepare()
    #checkHadrSuccess()
    eval(fun_name)()

main()

