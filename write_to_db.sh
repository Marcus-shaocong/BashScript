#!/bin/bash
#set -x
 USER="root"
 PASS="123456"

 if [ $# -ne 1 ]
 then
	 echo $0 DATEFILE
	 echo
	 exit 2
fi

data=$1

while read line;
do
	oldIFS=$IFS
	IFS=,
	echo $line
	values=($line)
	
	values[1]="\"`echo ${values[1]} | tr ' ' '#' `\""
	values[3]="\"`echo ${values[3]}`\""

	IFS=$oldIFS
	#echo ${values[@]}
	query=`echo ${values[@]} | tr '#' ', '`
	query=`echo $query | tr ' ' ', '`
	echo $query

	mysql -u $USER -p$PASS students <<EOF 
 INSERT INTO students VALUES($query); 
EOF

done< $data
echo Wrote data into DB
