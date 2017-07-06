#!/bin/bash

name="CoarseGrainedExecutorBackend"
pids=`jps | grep $name |  grep -o "^[0-9]*"`
#pids=`jps | grep -o "^[0-9]*"`
#echo $pids
./killtop&
user=`whoami`
top -u $user > toplog

for val in $pids; do
    #echo $val
    cat toplog | grep $val | awk -F " " '{print $6}'
done
