#!/bin/bash
s=0.5
c=0.5
d=0.5
echo " " 1> res.txt

for fl in "datasets"/*; do
	echo "datafile: $fl"
	START=$(date +%s.%N)
	for i in $(seq 9); do
		echo "$i iteration for $fl"
		python run.py -f $fl -s $s -c $c -d $d 1>> /dev/null
	done
	echo "last iteration for $fl"
	python run.py -f $fl -s $s -c $c -d $d -v 1>> res.txt
	END=$(date +%s.%N)
	
	DIFF=$(echo "$END - $START" | bc)
	echo "datafile: $fl; time: $DIFF"
done