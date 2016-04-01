#!/bin/bash
su sybpi1 << EOF!!
#Sybase123
EOF!!
LANG=C
. /sybase/PI1/SYBASE.sh
isql -Usapsa -PSybase123 -SPI1 -X -w999 <<EOF!!
use master
go
disk init name='PI1_log_002',physname='/sybase/PI1/saplog_1/PI1_log_002.dat',size='20G'
go
disk init name='PI1_data_002',physname='/sybase/PI1/sapdata_1/PI1_data_002.dat',size='40G'
go
alter database PI1 on PI1_data_002='40G' log on PI1_log_002='20G'
go
use PI1
go
checkpoint
go
use master
go
sp_dboption PI1,'trunc log on chkpt',true
go
quit
EOF!!
