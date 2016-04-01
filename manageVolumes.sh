#!/bin/bash
name=xdata
pvcreate /dev/$name
vgcreate vg_hadr /dev/$name
lvcreate -l 100%FREE -n lv_hadr vg_hadr
mkfs.ext3 /dev/vg_hadr/lv_hadr
mkdir /hadr
mount /dev/vg_hadr/lv_hadr /hadr
echo "/dev/vg_hadr/lv_hadr /hadr ext3 rw,noatime 0 0">>/etc/fstab #自动挂载硬盘
df -h
mkdir '/hadr/sybase'
sudo ln -s /hadr/sybase /sybase
mkdir '/hadr/sapmnt'
sudo ln -s /hadr/sapmnt /sapmnt
mkdir '/hadr/usr_sap'
sudo ln -s /hadr/usr_sap /usr/sap
