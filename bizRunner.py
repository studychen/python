
from my_util import ase_adapter as adapter
import sys
import time

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "biz runner error, try python bizRunner.py envid job_name wait_time"
        sys.exit(-1)
    envid = str(sys.argv[1])
    job_name = str(sys.argv[2])
    wait_time = int(sys.argv[3])
    cur = adapter.init()
    sql = "insert into bizsuite_job_request values(" + envid + ",\"" + job_name + "\"," + "\"pending\",1)"
    cur[0].execute(sql)
    cur[1].commit()
    sql = "select job_status from bizsuite_job_request where env_id = " + envid
    while wait_time > 0:
        cur[0].execute(sql)
        rows = cur[0].fetchall()
        if len(rows) < 1:
            sys.exit(-1)
        if rows[0][0] == "finished":
            sys.exit(0)
        else:
            wait_time -= 5
        time.sleep(5)
    sys.exit(-1)



