#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
else
	shikona=$1
	python3 ~/sumodb/scripts/rikishi.py "$shikona"
	if [ $?  == 1 ]
	then
		echo "Shikona not found"
	fi
fi
