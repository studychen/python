from subprocess import Popen
import time
import sys
import os
import time

def prepare():
    filename = r'C:\sumScripts\sum.info'
    global nw_ip,sid,instance_number
    while(1):
        if os.path.exists(filename):
            message = 'OK, the "%s" file exists. Wait for 3s'
            print message  % filename
            time.sleep(3)
            infoFile = open(filename)
            nw_ip=infoFile.readline().strip('\n')
            sid=infoFile.readline().strip('\n')
            instance_number=infoFile.readline().strip('\n')
            print '============ip '+nw_ip +' ==========='
            print '============sid '+sid+' ==========='
            print '=====instance_number '+instance_number+' ========='
            infoFile.close()
            os.remove(filename)
            break
        else:
            message = 'Wait, the "%s" file not exists.'
            print message % filename
        time.sleep(2)

    # if len(sys.argv) != 4:
    #     print 'usage: python install.py <ip> <sid> <instance_num>'
    #     sys.exit(-1)
    # nw_ip = sys.argv[1]
    # sid = sys.argv[2]
    # instance_number = sys.argv[3]


def openSapgui():
    command = [r'C:\sumScripts\open_sapgui.bat', nw_ip, sid, instance_number]
    #print command
    p = Popen(command, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    time.sleep(5)

def logonSystem():
    vbscript = r"C:\sumScripts\logon.bat"
    p = Popen(vbscript, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()

def killSapgui():
    command = [r'C:\sumScripts\kill_sapgui.bat']
    #print command
    p = Popen(command, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()

def handleCoprightDialog():
    print '============ handleCoprightDialog start ==============='
    openSapgui()
    time.sleep(5)
    logonSystem()
    time.sleep(5)
    killSapgui()
    time.sleep(5)
    print '============ handleCoprightDialog succeed ==============='

def createNewUser():
    openSapgui()
    print '============ createNewUser start =============='
    vbscript = r"C:\sumScripts\ddic_logon.bat"
    p = Popen(vbscript, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    vbscript = r"C:\sumScripts\create_newuser.bat"
    p = Popen(vbscript, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    print '============ createNewUser end ================'

def changeUserPasswd():
    openSapgui()
    print '======= changeUserPasswd start ============='
    vbscript = r"C:\sumScripts\newuser_logon.bat"
    p = Popen(vbscript, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    print '======= change NewUser passwd succeed ============='

def runVBScript(task_name):
    openSapgui()
    print '============task '+ task_name+ ' running =============='
    vbscript = r"C:\sumScripts\sumlogon.bat"
    sumLog=open('logs\sum.log', 'a')
    nowTime = time.gmtime()
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", nowTime)
    sumLog.write(timeStr + ' on ' + nw_ip + ' '+ task_name + ' start\n')
    sumLog.close()
    p = Popen(vbscript, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    # \\" is need & not add r to "C:\sumScripts\\"
    vbscript = "C:\sumScripts\\" + task_name + ".bat"
    p = Popen([vbscript, nw_ip, sid], cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    sumLog=open('logs\sum.log', 'a')
    nowTime = time.gmtime()
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S", nowTime)
    sumLog.write(timeStr + ' on ' + nw_ip + ' '+ task_name +' succeed\n')
    sumLog.close()
    print '============task '+ task_name+ ' succeed =============='

def returnFile():
    print '============ returnFile start ==============='
    sumInfo=open('sumgui.return', 'w')
    sumInfo.write('0')
    sumInfo.close()
    command = ['pscp.exe', '-pw', 'Sybase123', 'sumgui.return', 'root@10.173.1.65:/hadr/sumAuto/code']
    # print command
    p = Popen(command, cwd=r"C:\sumScripts")
    stdout, stderr = p.communicate()
    print '============ returnFile succeed ==============='

def startWeb():
    print '============ startWeb start ==============='
    sumIp = 'http://'+nw_ip +':4239'
    os.system('start ' + sumIp)
    print '============ startWeb succeed ==============='


def main():
    print '============ another new whole sumSapgui start ==============='
    prepare()
    time.sleep(2)
    handleCoprightDialog()
    createNewUser()
    changeUserPasswd()
    runVBScript('stms')
    runVBScript('sm59')
    runVBScript('spam')
    runVBScript('note')
    runVBScript('se09')
    returnFile()

while (1):
    main()
    time.sleep(5)



