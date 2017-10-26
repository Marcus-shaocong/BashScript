#!/bin/bash
#set -x
log=/var/log/wtmp

if [[ -n $1 ]];
then 
	log=$1
fi

printf "%-4s %-10s %-10s %-6s %-8s\n" "Rank" "User" "Start" "Logins" "Usage hours"

last -f $log | head -n -2 > /tmp/ulog.$$

cat /tmp/ulog.$$ | cut -d' ' -f1 | sort | uniq > /tmp/users.$$

( 
while read user;
do
	grep ^$user /tmp/ulog.$$ > /tmp/user.$$
	minutes=0

	while read t 
	do
		if [[ $t != "in" ]]
		then
			s=$(echo $t | awk -F: '{ print ($1 * 60) + $2}')
			let minutes=minutes+s
		fi
	done< <(cat /tmp/user.$$ | awk '{ print $NF}' | tr -d ')(' )

	firstlog=$(tail -n 1 /tmp/user.$$ | awk '{ print $5,$6 }')
	nlogins=$(cat /tmp/user.$$ | wc -l)
	hours=$(echo "$minutes /60.0" | bc)

	printf "%-10s %-10s %-6s %-8s\n" $user "$firstlog" $nlogins $hours

done< /tmp/users.$$

) | sort -nrk 4 | awk '{ printf("%-4s %s\n", NR,$0 )}'




