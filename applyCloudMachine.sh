#!/bin/bash
if [ $# -ne 4 ]
then
	echo "usage: bash applymachine.sh <project> <windows/linux> <volsize> <describe>"
	exit -1
fi

which=$1
if [ $2 = "windows" ]
then
	machine=WINDOWS-2008R2-x86_64
elif [ $2 = "linux" ]
then
	machine=SAP-SLES11-SP3-x86_64
fi
volumesize=$3
instanceDes=$4
personid=i316736
instanceLog=$instanceDes.log
instanceInfo=$instanceDes.info
applyTime=`date +%Y_%m_%d_%H_%M_%S`
logFolder=$instanceDes
size=medium_2_4
mkdir $logFolder
chmod 777 $logFolder
cd ./$logFolder && touch $instanceLog && cd ..


export EC2_HOME=/usr/local/ec2/ec2-api-tools-1.7.3.2
export PATH=$PATH:$EC2_HOME/bin
export JAVA_HOME=/usr/lib64/jvm/jre-1.7.0-ibm
export EC2_URL=https://ec2-us-west.api.monsoon.mo.sap.corp/

if [ $which = "my" ]
then
	echo "" >> ./$logFolder/$instanceLog
	echo "===================================" >> ./$logFolder/$instanceLog
	echo "===                             ===" >> ./$logFolder/$instanceLog
	echo "===    TomChen project          ===" >> ./$logFolder/$instanceLog
	echo "===                             ===" >> ./$logFolder/$instanceLog
	echo "===================================" >> ./$logFolder/$instanceLog
    export AWS_ACCESS_KEY=STMxNjczNjo6MTYyOTk%3D%0A
    export AWS_SECRET_KEY=gmfihKr%2FGne93rfME%2B5MER5G%2Bbgv2ZVMXTni%2F1pCCEc%3D%0A
elif [ $which = "hadr" ]
then
	echo "" >> ./$logFolder/$instanceLog
	echo "===================================" >> ./$logFolder/$instanceLog
	echo "===                             ===" >> ./$logFolder/$instanceLog
	echo "===    Hadr_Auto project        ===" >> ./$logFolder/$instanceLog
	echo "===                             ===" >> ./$logFolder/$instanceLog
	echo "===================================" >> ./$logFolder/$instanceLog
    export AWS_ACCESS_KEY=STMxNjczNjo6MTA2MzU%3D%0A
    export AWS_SECRET_KEY=WzrwEtl%2FMcCDw0mW5htAvz4OM2u5Oz3XasGu0kO5TV4%3D%0A
fi

echo ""
echo "===================================" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===    Create Monsoon Instance  ===" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===================================" >> ./$logFolder/$instanceLog

ec2-run-instances $machine -t $size -z dublin_1 1> ./$logFolder/ec2run.out 2>&1
STATUS=$?
if [ $STATUS != 0 ]
then
	cat  ./$logFolder/ec2run.out
	echo "ERROR: ec2-run-instance returned $STATUS"  >> ./$logFolder/$instanceLog
	exit $STATUS
fi

#cat ec2run.out
INS_NAME=`cat ./$logFolder/ec2run.out | grep INSTANCE | awk '{ print $2 }'`
INS_STATE=`cat ./$logFolder/ec2run.out | grep INSTANCE | awk '{ print $4 }'`
echo "Instance $INS_NAME is $INS_STATE" >> ./$logFolder/$instanceLog

ec2-describe-instances | grep INSTANCE | grep $INS_NAME 1> ./$logFolder/ec2din.out 2>&1
#cat /ec2din.out
INS_STATE=`cat ./$logFolder/ec2din.out | awk '{ print $6 }'`
echo "--------Instance state: $INS_STATE---------------" >> ./$logFolder/$instanceLog
while [ x$INS_STATE !=  "xrunning" ]
do
	sleep 20
	ec2-describe-instances | grep INSTANCE | grep $INS_NAME 1> ./$logFolder/ec2din.out 2>&1
	#cat /ec2din.out
	INS_STATE=`cat ./$logFolder/ec2din.out | awk '{ print $6 }'`
	echo "Instance $INS_NAME is $INS_STATE" >> ./$logFolder/$instanceLog
done

HOST=${INS_NAME}.mo.sap.corp

echo $INS_NAME >> ./$logFolder/$instanceInfo #mo-213131
echo $HOST>> ./$logFolder/$instanceInfo #mo-213131.mo.sap.corp

#change instance name in the web page
if [ $which = "my" ]
then 
	toolbox organization set i316736 --global
	toolbox project set tomchen --global
	toolbox instance update --name=$instanceDes --description=$instanceDes $INS_NAME
elif [ $which = "hadr" ]
then
	toolbox organization set hana_dms --global
	toolbox project set hadr_auto --global
	toolbox instance update --name=$instanceDes --description=$instanceDes $INS_NAME
fi

echo "" >> ./$logFolder/$instanceLog
echo "===================================" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===    Create Monsoon Volume    ===" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===================================" >> ./$logFolder/$instanceLog

ec2-create-volume --size $volumesize --availability-zone dublin_1 1> ./$logFolder/ec2cv.out 2>&1 2>&1
VOL_STATE=$?
if [ $VOL_STATE != 0 ]
then
    cat ./$logFolder/ec2log.out
    echo "ERROR: ec2-create-volume return $VOL_STATE" >> ./$logFolder/$instanceLog
    exit $VOL_STATE
fi

VOL_NAME=`cat ./$logFolder/ec2cv.out | grep VOLUME | awk '{print $2}'`
VOL_STATE=`cat ./$logFolder/ec2cv.out | grep VOLUME | awk '{print $5}'`
echo "Volume $VOL_NAME is $VOL_STATE" >> ./$logFolder/$instanceLog
ec2-describe-volumes | grep VOLUME | grep $VOL_NAME 1> ./$logFolder/ec2dv.out 2>&1
VOL_STATE=`cat ./$logFolder/ec2dv.out | awk '{print $5}'`
while [ x$VOL_STATE != x"available" ]
do 
	sleep 10
	ec2-describe-volumes | grep VOLUME | grep $VOL_NAME 1> ./$logFolder/ec2dv.out 2>&1
	VOL_STATE=`cat ./$logFolder/ec2dv.out | awk '{print $5}'`
	echo "Volume $VOL_NAME is $VOL_STATE" >> ./$logFolder/$instanceLog
done

echo ""
echo "===================================" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===    Attach Monsoon Volume    ===" >> ./$logFolder/$instanceLog
echo "===                             ===" >> ./$logFolder/$instanceLog
echo "===================================" >> ./$logFolder/$instanceLog
echo "Attach Volume $VOL_NAME to Instance $INS_NAME" >> ./$logFolder/$instanceLog
ec2-attach-volume $VOL_NAME --instance $INS_NAME --device xdata 1> ./$logFolder/ec2av.out 2>&1
STATUS=$?
if [ $STATUS != 0 ]
then
	cat ./$logFolder/ec2av.out
	echo "ERROR: ec2-attach-volume returned $STATUS" >> ./$logFolder/$instanceLog
	exit $STATUS
fi

VOL_STATE=`cat ./$logFolder/ec2cv.out | grep VOLUME | awk '{print $5}'`
echo "Volume $VOL_NAME is $VOL_STATE" >> ./$logFolder/$instanceLog
ec2-describe-volumes | grep ATTACHMENT | grep $VOL_NAME 1> ./$logFolder/ec2dv.out 2>&1
VOL_STATE=`cat ./$logFolder/ec2dv.out | awk '{print $5}'`
while [ x$VOL_STATE != x"attached" ]
do 
	sleep 10
	ec2-describe-volumes | grep ATTACHMENT | grep $VOL_NAME 1> ./$logFolder/ec2dv.out 2>&1
	VOL_STATE=`cat ./$logFolder/ec2dv.out | awk '{print $5}'`
	echo "Volume $VOL_NAME is $VOL_STATE" >> ./$logFolder/$instanceLog
done

#using ssh attch volume 
if [ $2 = "linux" ]
then
	SSH="ssh -t -o StrictHostKeyChecking=no $personid@$HOST"
	$SSH 'sudo /sbin/pvcreate /dev/xdata' >> ./$logFolder/$instanceLog
	$SSH 'sudo /sbin/vgcreate vg_hdbdata /dev/xdata' >> ./$logFolder/$instanceLog
	$SSH 'sudo /sbin/lvcreate -l 100%FREE -n lv_hdbdata vg_hdbdata'  >> ./$logFolder/$instanceLog
	$SSH 'sudo /sbin/mkfs.ext3 /dev/vg_hdbdata/lv_hdbdata' >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/mkdir /hadr' >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/mount /dev/vg_hdbdata/lv_hdbdata /hadr' >> ./$logFolder/$instanceLog
	echo "===    SSH mount volume end     ===" >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/df -h' >> ./$logFolder/$instanceLog
	#$SSH 'sudo /bin/echo "/dev/vg_hdbdata/lv_hdbdata /hadr ext3 rw,noatime 0 0">>/etc/fstab'
	$SSH 'sudo /bin/mkdir /hadr/sybase && sudo /bin/mkdir /hadr/sapmnt && sudo /bin/mkdir /hadr/usr_sap' >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/mkdir /hadr/packages' >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/ln -s /hadr/sybase /sybase && sudo /bin/ln -s /hadr/sapmnt /sapmnt && sudo /bin/ln -s /hadr/usr_sap /usr/sap' >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/chmod 777 -R /hadr/packages' >> ./$logFolder/$instanceLog
	echo "===    Set link end             ===" >> ./$logFolder/$instanceLog
	$SSH '(echo "Sybase123"
	sleep 1
	echo "Sybase123")|sudo passwd root' >> ./$logFolder/$instanceLog
	echo "===    Change passwd end        ===" >> ./$logFolder/$instanceLog
	echo "===    name: $instanceDes  IP    is      ===" >> ./$logFolder/$instanceLog
	$SSH 'sudo /bin/hostname -i' >> ./$logFolder/$instanceLog
    $SSH 'sudo /bin/hostname -i' >> ./$logFolder/$instanceInfo
fi

