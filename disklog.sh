#!/bin/bash
#set -x
logfile="diskusage.log"

if [[ -n $1 ]]
then
	logfile=$1
fi

if [ ! -e $logfile ]
then
	printf "%-8s %-14s %-9s %-8s %-6s %-6s %-6s %s\n" "Date" "IP address" "Device" "Capacity" "User" "Free" "Percent" "Status" > $logfile

fi

IP_LIST="10.141.59.221"

(
	for ip in $IP_LIST;
	do
		ssh c4dev@$ip 'df -H ~/tmp' | grep ^/dev/ > /tmp/$$.df

		while read line;
		do
			cur_date=$(date +%D)
			printf "%-8s %-14s " $cur_date $ip
			echo $line | awk '{ printf("%-9s %-8s %-6s %-6s %-8s", $1,$2,$3,$4,$5);}'
			pusg=$(echo $line | egrep -o "[0-9]+%")
			pusg=${pusg/\%/}
			if [ $pusg -lt 80 ];
			then
				echo SAFE
			else
				echo ALERT
			fi
		done< /tmp/$$.df

	done

) >> $logfile

cat $logfile
