#using ssh attch volume 
personid=**userid**
Hos=$1
HOST=${Hos}.mo.sap.corp
SSH="ssh -t -o StrictHostKeyChecking=no $personid@$HOST"
$SSH 'sudo /sbin/pvcreate /dev/xdata' 
$SSH 'sudo /sbin/vgcreate vg_hdbdata /dev/xdata' 
$SSH 'sudo /sbin/lvcreate -l 100%FREE -n lv_hdbdata vg_hdbdata'  
$SSH 'sudo /sbin/mkfs.ext3 /dev/vg_hdbdata/lv_hdbdata' 
$SSH 'sudo /bin/mkdir /hadr' 
$SSH 'sudo /bin/mount /dev/vg_hdbdata/lv_hdbdata /hadr' 
$SSH 'sudo /bin/echo "/dev/vg_hdbdata/lv_hdbdata /hadr ext3 rw,noatime 0 0" >> /etc/fstab'
echo "===    SSH mount volume end     ===" 
$SSH 'sudo /bin/df -h' 
$SSH 'sudo /bin/echo "/dev/vg_hdbdata/lv_hdbdata /hadr ext3 rw,noatime 0 0">>/etc/fstab'
$SSH 'sudo /bin/mkdir /hadr/sybase && sudo /bin/mkdir /hadr/sapmnt && sudo /bin/mkdir /hadr/usr_sap' 
$SSH 'sudo /bin/mkdir /hadr/packages' 
$SSH 'sudo /bin/ln -s /hadr/sybase /sybase && sudo /bin/ln -s /hadr/sapmnt /sapmnt && sudo /bin/ln -s /hadr/usr_sap /usr/sap' 
$SSH 'sudo /bin/chmod 777 -R /hadr/packages' 
echo "===    Set link end             ===" 
$SSH '(echo "passwd123"
sleep 1
echo "passwd123")|sudo passwd root' 
echo "===    Change passwd end        ===" 
echo "===    name: $instanceDes  IP    is      ===" 
$SSH 'sudo /bin/hostname -i' 
$SSH 'sudo /bin/hostname -i'  
