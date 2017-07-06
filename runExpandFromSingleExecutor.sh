#!/bin/bash

dir_kmeans="~/scala/KMeans-cluster"
dir_graph="~/scala/Spark-Graphx"

kmeans="kmeans"
kmeans500="kmeans500"
kmeans1G="kmeans1G"

bfs="bfs"
bfs_larger="bfs_larger"

pr="pr"
pr_larger="pr_larger"

function replaceDatafile(){
    filename=$1
    script=$2
    num=`cat $script | grep -n file: | sed -n 1p | awk -F ":" '{print $1}'`
    #sed -i "${num}s/file:.*/guolei/" $script
    #cat $script | sed "${num}s/file:.*/file:\/home\/guolei\/benchmarkdata\/${filename}/"
    sed -i "${num}s/file:[^ ]*/file:\/home\/guolei\/benchmarkdata\/${filename}/" $script
    #cat $script
}

function singleExecutorTest(){
    dir=$1
    app=$2
    str=$dir" "$app
    echo $str > config.run
}

basedir="/home/guolei/sparkInfo"

function test(){
    app=$1
    data=$2
    dir=$3

    cd $dir
    replaceDatafile $data $app
    cd $basedir
    str=$dir" "$app
    echo $str > config.run
    ./singleExecutor.py
}

kmeans_args=(
data-Kmeans_200M
data-Kmeans_500M
data-Kmeans_1G
)

graph_args=(
Facebook_genGragh_27M.txt
Facebook_genGragh_60M.txt
Facebook_genGragh_137M.txt
Facebook_genGragh_307M.txt
Facebook_genGragh_667M.txt
)

text_args=(
lda_wiki1w_1G
lda_wiki1w_2G
lda_wiki1w_3G
lda_wiki1w_4G
lda_wiki1w_5G
)

naivebayesTrainer_args=(
naivebayesdata_1G
naivebayesdata_2G
naivebayesdata_3G
naivebayesdata_4G
)

naivebayes_args=(
naivebayesdata_119M
naivebayesdata_244M
naivebayesdata_490M
naivebayesdata_1G
)

rm singleResult

function testSingle(){
    for v in ${text_args[*]}
    do
        echo $v
        #test wc $v                           "/home/guolei/scala/WordCount-cluster"
    done
    #test wc                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/WordCount-cluster"
    for v in ${kmeans_args[*]}
    do
        echo $v
        #test kmeans $v                       "/home/guolei/scala/KMeans-cluster"
        #exit
    done

    for v in ${graph_args[*]}
    do
        echo $v
        #test bfs $v                           "/home/guolei/scala/Spark-Graphx"
    done

    for v in ${graph_args[*]}
    do
        echo $v
        test pr  $v                          "/home/guolei/scala/Spark-Graphx"
    done

    for v in ${graph_args[*]}
    do
        echo $v
        #test lp $v                           "/home/guolei/scala/Spark-Graphx"
    done
    #test lp                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/Spark-Graphx"

    for v in ${graph_args[*]}
    do
        echo $v
        #test cc $v                           "/home/guolei/scala/Spark-Graphx"
    done
    #test cc                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/Spark-Graphx"
    for v in ${naivebayesTrainer_args[*]}
    do
        echo $v
        #test nbt $v                          "/home/guolei/scala/NaiveBayesTrainer"
    done
    #test nbt                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/NaiveBayesTrainer"

    for v in ${naivebayes_args[*]}
    do
        echo $v
        #test nb  $v                          "/home/guolei/scala/NaiveBayes"
    done
    #test nb                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/NaiveBayes"

    for v in ${text_args[*]}
    do
        echo $v
        #test sort $v                         "/home/guolei/scala/Sort"
    done
    #test sort                            "1 2 3 4 5 6 7 8 9" "/home/guolei/scala/Sort"
}

echo -e "case\tmemoryPerNode\tcoresPerNode\texecutors\truntime" > singleResult
./restart
testSingle
exit


#for val in 1 2 3 4 5; do
for val in 3; do
    echo $val
    changeMemory $val
    #testAll
    testSingle
done

#singleExecutorTest $dir_kmeans $kmeans
#singleExecutorTest $dir_kmeans $kmeans500
#singleExecutorTest $dir_kmeans $kmeans1G

#singleExecutorTest $dir_graph $bfs
#singleExecutorTest $dir_graph $bfs_larger

singleExecutorTest $dir_graph $pr
#singleExecutorTest $dir_graph $pr_larger

./singleExecutor.py
