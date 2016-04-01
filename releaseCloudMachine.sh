#!/bin/bash
if [ $# -ne 2 ]
then
	echo "usage: bash releaseMachine.sh <project my/hadr> <instanceId>"
	exit -1
fi

which=$1
instanceId=$2

if [ $which = "my" ]
then
	echo ""
	echo "==================================="
	echo "===                             ==="
	echo "===    TomChen project          ==="
	echo "===                             ==="
	echo "==================================="
    export AWS_ACCESS_KEY=STMxNjczNjo6MTYyOTk%3D%0A
    export AWS_SECRET_KEY=gmfihKr%2FGne93rfME%2B5MER5G%2Bbgv2ZVMXTni%2F1pCCEc%3D%0A
elif [ $which = "hadr" ]
then
	echo ""
	echo "==================================="
	echo "===                             ==="
	echo "===    Hadr_Auto project        ==="
	echo "===                             ==="
	echo "==================================="
    export AWS_ACCESS_KEY=STMxNjczNjo6MTA2MzU%3D%0A
    export AWS_SECRET_KEY=WzrwEtl%2FMcCDw0mW5htAvz4OM2u5Oz3XasGu0kO5TV4%3D%0A
fi


#mo-6e423496b
volumeId=`ec2-describe-volumes | grep $instanceId | awk '{print $2}'`

echo "volume id is $volumeId"
#ec2-delete-volume $volumeId
state=$?
if [ $state != 0 ]
then
	echo 'ec2-delete-volume failed with $state'
	exit $state
fi
echo "===    delete volume end         ==="

echo "instances id is $instanceId"
#ec2-terminate-instances $instanceId
state=$?
if [ $state != 0 ]
then
	echo 'ec2-terminate-instances failed with $state'
	exit $state
fi
echo "===    terminate instances end    ==="
 