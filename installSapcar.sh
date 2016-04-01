#! /bin/sh
echo ""
echo "=================install sapcar    =================="
#The second EOF must thus written
expect << EOF
	spawn zypper in sapcar
	set timeout 120
	expect {
			"options] (y):" {send "y\r";exp_continue}
			"yes/no] (no):" {send "yes\r";exp_continue}
	}
EOF
echo "=================install sapcar end =================="
