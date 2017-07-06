#!/bin/bash

cat ~/spark/spark-2.1.0/conf/spark-defaults.conf | grep "spark.executor.cores" | awk -F " " '{print $2}'
