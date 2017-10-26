#!/bin/bash
###
# usage message_user.sh username < message.txt
#set -x
USERNAME=$1
devices=`ls /dev/pts/* -l | awk '{ print $3, $10 }' | grep $USERNAME | awk '{print $2}'`

for dev in $devices;
do
	cat /dev/stdin > $dev
done
