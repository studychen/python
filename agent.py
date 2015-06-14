from subprocess import Popen
import sybpydb
import time
import sys

task_name = 'null';
nw_ip = 'null'
sid = 'NW7'
job_id = 9999
instance_number = '00'
agent_hostname='unknow'

def getJobFromDatabase():
	global task_name
	global nw_ip
	global sid
	global job_id
	global instance_number
	has_job = False
	pending_job_count = 0
	conn = sybpydb.connect(user='sa', password='Sybase123', servername='TIA')
	cur = conn.cursor()
	cur.execute("begin transaction")
	cur.execute("use hadr")
	cur.execute("lock table bizsuite_job_request in exclusive mode")
	cur.execute("select top 1 bizsuite_job_request.id, bizsuite_job_request.job_name, hadrenv.primaryip, hadrenv.sid, hadrenv.instanceNumber from bizsuite_job_request, hadrenv where bizsuite_job_request.job_status='pending' and hadrenv.id=bizsuite_job_request.env_id order by id")
	row = cur.fetchall()
	pending_job_count = len(row)
	if(pending_job_count == 1):
		job_id = row[0][0]
		task_name = row[0][1]
		nw_ip = row[0][2]
		sid = row[0][3]
		instance_number = row[0][4]
		print "execute " + task_name + " on " + nw_ip + " with sid " + sid + " and instance number " + instance_number
		updateSql = "update bizsuite_job_request set job_status='in_progress' where id=" + str(job_id)
		print updateSql
		cur.execute(updateSql)
		cur.execute("commit transaction")
		has_job = True
	else:
		cur.execute("commit transaction")
	cur.close()
	conn.close()
	return has_job
	
def updateAgentStatus():
	conn = sybpydb.connect(user='sa', password='Sybase123', servername='TIA')
	cur = conn.cursor()
	cur.execute("use hadr")
	updateSql = "update bizsuite_job_request set job_status='finished' where id=" + str(job_id)
	print updateSql
	cur.execute(updateSql)
	conn.commit()
	cur.close()
	conn.close()
	
def runVBScript():
	global nw_ip
	global sid
	global instance_number
	vbscript = task_name + ".bat"
	p = Popen([vbscript, nw_ip, sid, instance_number], cwd=r"C:\hadrTest_741\vbs")
	stdout, stderr = p.communicate()

def openSapgui():
	global nw_ip
	global sid
	global instance_number
	command = ['open_sapgui.bat', nw_ip, sid, instance_number]
	#print command
	p = Popen(command, cwd=r"C:\hadrTest_741\vbs")
	stdout, stderr = p.communicate()

def logonSystem():
	vbscript = "logon.bat"
	p = Popen(vbscript, cwd=r"C:\hadrTest_741\vbs")
	stdout, stderr = p.communicate()
	
def killSapgui():
	command = ['kill_sapgui.bat']
	#print command
	p = Popen(command, cwd=r"C:\hadrTest_741\vbs")
	stdout, stderr = p.communicate()

def handleCoprightDialog():
	openSapgui()
	logonSystem()
	killSapgui()
	time.sleep(5)
	
def needUpdate():
	global agent_hostname
	conn = sybpydb.connect(user='sa', password='Sybase123', servername='TIA')
	cur = conn.cursor()
	cur.execute("use hadr")
	need_update = False
	cur.execute("select need_code_update from agent where hostname='" + agent_hostname + "'")
	row = cur.fetchall()
	if(len(row) == 0):
		print 'agent is not registered in the agent table' 
	if(len(row) > 1):
		print 'there are more than one agent with agent_hostname ' + agent_hostname + ' in the agent table'
	if(len(row) == 1):
		need_update_code=row[0][0]
		if(need_update_code == 'true'):
			print 'need update code on ' + agent_hostname
			need_update = True
			update_cmd = "update agent set need_code_update='false' where hostname='" + agent_hostname + "'"
			print update_cmd
			cur.execute(update_cmd)
			conn.commit()
	cur.close()
	conn.close()
	return need_update

def copyNewestCode():
	command = ['code_update.bat']
	p = Popen(command, cwd=r"C:\hadrTest_741\vbs")
	stdout, stderr = p.communicate()	
	
def updateCode():
	copyNewestCode()
	sys.exit(1)

def retrieveIP():
	global agent_hostname
	if (len(sys.argv) != 2):
		print 'wrong args, usage: ' + sys.argv[0] + ' ip_address_of_this_agent'
		sys.exit(1)
	agent_hostname = sys.argv[1]
	
while(1):
	retrieveIP()
	if(needUpdate()):
		updateCode()
	if(getJobFromDatabase()):
		handleCoprightDialog()
		openSapgui()
		time.sleep(5)
		logonSystem()
		runVBScript()
		updateAgentStatus()
	print 'scanning: no job request'
	time.sleep(5)



