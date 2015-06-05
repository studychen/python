from subprocess import Popen
import subprocess
import threading,time
    # numThread = 5
# total = 10001
# per = total / numThread

startn = 1
endn = 300001
step =1000
total = (endn - startn + 1 ) /step
for i in xrange(total):
    startNumber = startn + step * i
    p1=Popen(['python', 'ruisi.py', str(startNumber),str(startNumber + step)],bufsize=10000, stdout=subprocess.PIPE)
    print '%s - %s download start... ' %(startNumber, startNumber + step)
    p1.communicate()
    time.sleep(5)
