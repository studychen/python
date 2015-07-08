__author__ = 'I316736'
import sys
import subprocess
import threading
from subprocess import Popen
def cleanSingleMachine(ip,sid):
    print '=================cleanHadrEnv on ' + ip + ' running ... =================='
    subprocess.call('./pscp -pw Sybase123 cleanHadrEnv.sh root@'+ ip+ ':/root' ,shell=True)
    result = subprocess.call('./plink -pw Sybase123 root@'+ ip + ' bash cleanHadrEnv.sh ' + sid, shell=True)
    if result != 0:
        print '=================cleanHadrenv on ' + ip + ' error     =================='
        sys.exit(-1)
    print '=================clean Share Memory running ...=================='
    p=Popen(['java', '-jar', './cleanEnv.jar', ip])
    p.communicate()
    print '=================clean Share Memory succeed=================='
    print '=================cleanHadrEnv on ' + ip + ' succeed     =================='

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: python cleanHadrEnv.py {sid} {pri_ip} {sta_ip}"
        sys.exit(-1)
    sid = sys.argv[1]
    priIp = sys.argv[2]
    staIp=sys.argv[3]
    cleanPriIp = threading.Thread(target=cleanSingleMachine, args=(priIp, sid,))
    cleanStaIp = threading.Thread(target=cleanSingleMachine, args=(staIp, sid,))
    cleanPriIp.start()
    cleanStaIp.start()


