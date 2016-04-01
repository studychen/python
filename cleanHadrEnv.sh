#!/bin/bash
#clear Hadr Env
#kill progress & remove folder & clear tmp 
if [ $# -ne 1 ]
then
	echo "usage: $0 <sid>"
	exit -1
else
	sid=$1
fi
sid_downcase=`echo $sid | tr "A-Z" "a-z"`
sid_uppercase=`echo $sid | tr "a-z" "A-Z"`
user1=${sid_downcase}adm
user2=syb${sid_downcase}

echo "===========stopsap r3 waiting...   =============="
if grep -q $user1 /etc/passwd
then 
	su - ${user1} -c 'stopsap r3'
	sleep 200
else 
	echo "user ${user1} not exists, not need stopsap r3"
fi
echo "===========stopsap r3 succeed      =============="

ps -ef | grep dataserver | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 dataserver 4901 port   =============="
	ps -ef | grep dataserver | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi

ps -ef | grep backupserver | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 backupserver 4902 & 4903 port =============="
	ps -ef | grep backupserver | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi
ps -ef | grep repserver | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 repserver 4905 port    =============="
	ps -ef | grep repserver | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi
ps -ef | grep dbsrv16 | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 dbsrv16 4906 port      =============="
	ps -ef | grep dbsrv16 | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi
ps -ef | grep dbltm | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 dbltm 4907 port        =============="
	ps -ef | grep dbltm | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi
ps -ef | grep java | grep $sid_uppercase >> /dev/null
if [ $? -eq 0 ]
then
	echo "============kill - 9 java 4908 & 4909 port         =============="
	ps -ef | grep java | grep $sid_uppercase | awk '{print $2}' | xargs kill -9
fi

echo "============remove /LABELIDX.ASC & hadrSilentInstall, waiting =============="
if [ -f /LABELIDX.ASC ]
then
	rm /LABELIDX.ASC
else 
	echo "/LABELIDX.ASC not exists, not need delete"
fi
if [ -d /hadrSilentInstall ]
then
	rm -rf /hadrSilentInstall
else 
	echo "/hadrSilentInstall not exists, not need delete"
fi
echo "============remove /LABELIDX.ASC & hadrSilentInstall, succeed =============="
echo "============remove /tmp/sap*, waiting...                    =============="
rm -rf /tmp/sap*
echo "============remove /tmp/sap*, succeed                    =============="
echo "============remove /sybase/${sid_uppercase} & /sybase/${sid_uppercase}_REP, waiting...=============="
rm -rf /sybase/$sid_uppercase && rm -rf /sybase/${sid_uppercase}_REP
echo "============remove /sybase/${sid_uppercase} & /sybase/${sid_uppercase}_REP, succeed   =============="
echo "============remove /sapmnt/${sid_uppercase}, waiting...                  =============="
rm -rf /sapmnt/${sid_uppercase}
echo "============remove /sapmnt/${sid_uppercase}, succeed                     =============="
echo "============remove /usr/sap/* , waiting...              =============="
if [ -d /usr/sap ]
then
	rm -rf /usr/sap/*
else
	echo "/usr/sap not exists, not need delete"
fi
echo "============remove /usr/sap/* , succeed                 =============="

echo "============delete users: ${user1} & ${user2}           =============="
if grep -q $user1 /etc/passwd
then 
	userdel -r $user1
else
	echo "user ${user1} not exists, not need delete"
fi
if grep -q $user2 /etc/passwd
then 
	userdel -r $user2
else
	echo "user ${user2} not exists, not need delete"
fi
echo "============delete users: ${user1} & ${user2},succeed   =============="

echo "============clear memory cache, waiting         =============="
sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"
echo "============clear memory cache, succeed         =============="

echo "============clear alias, waiting         =============="
if grep -q 'export LANG=en && source' /etc/bash.bashrc
then
	cp /etc/bash.bashrc /etc/bash_copy.bashrc
	sed -i '/export LANG=en && source/,$d' /etc/bash.bashrc
else
	echo "alias not exist in /etc/bash.bashrc, not need delete"
fi
echo "============clear alias, succeed         =============="

