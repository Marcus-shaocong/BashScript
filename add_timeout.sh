#!/bin/bash
timeout=1
get_state()
{
	oid=$1
	if [[ -z $oid ]]
	then
		oid="0x1800000001"
	fi
	echo "oid :$oid"
	state=`MluCli.exe objectops -b_careful -info -oid $oid | grep "Public State" | cut -d: -f2 | tr -d '\040\011\012\015'`
	while [[ $state != "Error" && $state != "Ready" ]]
	do 
		echo "$state"
		echo "Not ready"
		let timeout++
		if [[ timeout -eq 100000000 ]] 
		then 		
			break
		fi
	done
	if [[ $state = "Ready" ]] 
	then
		echo "Now ready"
		exit 2
	fi
}

run_with_timeout () { 
    local time=10
    if [[ $1 =~ ^[0-9]+$ ]]; then time=$1; shift; fi
    # Run in a subshell to avoid job control messages
    ( "$@" &
      child=$!
      # Avoid default notification in non-interactive shell for SIGTERM
      trap -- "" SIGTERM
      ( sleep $time
        kill $child 2> /dev/null ) &
      wait $child
    )
}

run_with_timeout 5 get_state "0x1800000002" 
echo "exit code $?"
