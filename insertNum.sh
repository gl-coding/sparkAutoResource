#!/bin/bash


function insert(){
    file=$1
    flag=`cat $file | grep ,`
    echo $flag
    if [ -n "$flag" ]; then
        return
    fi
    num=`cat $file | wc -l`
    for((i=1;i<=$num;i++));do
        echo $i
        sed -i "${i}s/^/${i},/" $file
    done
}

#insert train.bfs0
#insert train.bfs1
#insert train.bfs2

for ca in bfs cc kmeans lp nb nbt wc pr
do
    echo $ca
    f="train."$ca"0"
    insert $f
    f="train."$ca"1"
    insert $f
    f="train."$ca"2"
    insert $f
done
