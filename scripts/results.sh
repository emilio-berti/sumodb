#!/bin/bash

if [ "$#" -ne 2 ]
then
    echo "Illegal number of parameters"
else
	shikona=$1
	basho=$2
	python3 ~/sumodb/scripts/results.py "$shikona" "$basho"
	if [ $?  == 1 ]
	then
		echo "Shikona not found"
	fi
fi
