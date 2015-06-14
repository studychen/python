import sys
import os.path
from subprocess import Popen
from subprocess import call

def get_delta(file1, file2):
    f = open("out.txt", "wr")
    call(["diff", file1, file2], stdout = f) 
    f.close

def checksum():
    if len(sys.argv) != 7:
        print 'usage: python diff.py <aseHost1> <port1> <aseHost2> <port2> <SID> <password>'
        sys.exit();
    

    aseHost1 = '10.173.3.46'
    port1 = str(4901)
    aseHost2 = '10.137.14.168'
    port2 = str(4902)
    sid = 'NW7'
    database = sid.upper()
    password = 'Sybase123'
    file1 = aseHost1 + '_' + database + '_datalength.txt'
    file2 = aseHost2 + '_' + database + '_datalength.txt'
    f = open("/dev/null", "wr")
    p1=Popen(['java', '-jar', './sybdbchksum.jar', '-h' + aseHost1 + ':' + port1, '-d' + database, '-usapsa', '-p' + password, '-mdatalength'], stdout = f)
    p2=Popen(['java', '-jar', './sybdbchksum.jar', '-h' + aseHost2 + ':' + port2, '-d' + database, '-usapsa', '-p' + password, '-mdatalength'], stdout = f)
    p1.communicate()
    p2.communicate()
    print file1 + ' generated'
    print file2 + ' generated'
    
    if os.path.isfile(file1):
        print file1 + ' exsit'
    else:
        print file1 + ' not exsit'
        exit(-1)
    
    if os.path.isfile(file2):
        print file2 + ' exsit'
    else:
        print file2 + ' not exsit'
        exit(-1)
    get_delta(file1, file2)

def analyzeDelta():
    f = open("out.txt", "r")
    for line in f:
        if "<" in line:
            if "Timestamp" in line:
                continue
            if "rs_lastcommit" in line:
                continue
            if "rs_ticket_history" in line:
                continue
            if "Total" in line:
                continue
            print "databases are not in sync"
            f.seek(0)
            for errorline in f:
                print errorline
            f.close()
            exit(-1)
    f.close
    print "all data are in sync"
    exit(0)

def main():
    checksum()
    analyzeDelta()

main()
