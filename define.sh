#!/bin/bash

apikey="newkil"

if [ $# -ne 2 ]
then 
	echo -e "Usage: $0 WORD NUMBER"
	exit -1;
fi


curl --silent http://www.dictionaryapi.com/api/v1/references/learners/xml/$1?key=$apikey | \
	grep -o \<dt\>.*\</dt\>
	sed 's$</*[a-z]*>$$g' | \
	had -n $2 | nl
