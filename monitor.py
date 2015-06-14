__author__ = 'I311229'

import os
import threading
import time
import subprocess

from my_util import ase_adapter as adapter
import env


def branch_thread(name, row):
    hadr_env_id = row[0]
    sql = "select top 1 testcase.id,testtype.command from testcase, testtype where testcase.typeid = testtype.id and status = 'NEW' and testcase.hadrenvid = " + str(hadr_env_id) + " order by testcase.id"
    while 1:
        cur = adapter.init()
        cur[0].execute(sql)
        testcases = cur[0].fetchall()
        if len(testcases) == 0:  # contains no testcases will return success
            # Manually update branch status
            cur[0].execute("update hadrenv set status = 'NEW' where id = " + str(hadr_env_id))
            cur[1].commit()
            cur[0].close()
            cur[1].close()
            # print "Env id " + str(hadr_env_id) + " cannot find testcases, return"
            return
        testcase = testcases[0]
        testcase_id = testcase[0]
        command = testcase[1]
        nowtime = time.gmtime()
        timestr = time.strftime("%Y_%m_%d_%H_%M_%S", nowtime)
        print "Find testcase " + str(testcase_id) + " " + command + " on " + timestr
        cur[0].execute("update testcase set status = 'RUNNING',starttime= '" + time.strftime("%Y/%m/%d %H:%M:%S", nowtime) + "' where id = " + str(testcase_id))
        cur[1].commit()
        result = call_command(command, timestr, row, hadr_env_id)
        print "Env id " + str(hadr_env_id) + " testcase_id " + str(testcase_id) + " " + command + " test result is " + str(result) + " on " + timestr
        if result == 0:
            cur[0].execute("update testcase set status = 'SUCCESS',endtime = '" + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "' where id = " + str(testcase_id))
            cur[1].commit()
            print "Env id " + str(hadr_env_id) + " testcase_id " + str(testcase_id) + " " + " success"
        else:
            cur[0].execute("update testcase set status = 'FAIL' where id = " + str(testcase_id))
            cur[1].commit()
            cur[0].execute("update hadrenv set status = 'FAIL' where id = " + str(hadr_env_id))
            cur[1].commit()
            cur[0].close()
            cur[1].close()
            print "Env id " + str(hadr_env_id) + " testcase_id " + str(testcase_id) + " " + " error, return"
            return


def call_command(command, timestr, row, env_id):
    command = str(command)
    print "Origin command str " + command
    command = command.replace("{pri_ip}", str(row[1]))
    command = command.replace("{pri_host}", str(row[2]))
    command = command.replace("{sta_ip}", str(row[3]))
    command = command.replace("{sta_host}", str(row[4]))
    command = command.replace("{ase_port}", str(row[5]))
    command = command.replace("{rs_port}", str(row[6]))
    command = command.replace("{rma_port}", str(row[7]))
    command = command.replace("{sid}", str(row[8]))
    command = command.replace("{asepkg}", str(row[9]))
    command = command.replace("{rspkg}", str(row[10]))
    command = command.replace("{masterpkg}", str(row[11]))
    command = command.replace("{kernelpkg}", str(row[12]))
    command = command.replace("{exportpkg}", str(row[13]))
    command = command.replace("{bizsuite}", str(row[14]))
    command = command.replace("{platform}", str(row[15]))
    command = command.replace("{time}", str(timestr))
    command = command.replace("{dic}", str(env.directory))
    command = command.replace("{env_id}", str(env_id))
    print "Compose command str " + command
    return subprocess.call(command + " >> " + os.path.join(".", "log", str(row[1]) + "_" + str(timestr) + ".log 2>&1"), shell=True)


def fetch_all_branches():
    cur = adapter.init()
    cur[0].execute("select h.id, h.primaryip, h.primaryLogicalHostName, h.standbyip, h.standbyLogicalHostName, h.asePort, h.rsPort, h.rmaPort, h.sid, p.asepkg, p.rspkg, b.masterpkg, b.kernelpkg, b.exportpkg, b.name, p.name from platform as p, hadrenv as h, bizsuite as b where h.platformid = p.id and h.bizsuiteid = b.id and h.status='NEW'")
    rows = cur[0].fetchall()
    for row in rows:  # this should be multi-thread
        cur[0].execute("update hadrenv set status = 'RUNNING' where id = " + str(row[0]))
        cur[1].commit()
        # print "Update hadrenv " + str(row[0]) + " to RUNNING status"
        thread = threading.Thread(target=branch_thread, args=(1, row))
        thread.start()
    cur[0].close()
    cur[1].close()


if __name__ == '__main__':
    while 1:
        fetch_all_branches()
        time.sleep(5)


