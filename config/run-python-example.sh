#!/bin/bash

# test the hadoop cluster by running wordcount

# create input directory on HDFS
hadoop fs -mkdir -p input

# put input files to HDFS
hdfs dfs -put ./example.txt input/

# run wordcount
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input input/example.txt -output output

# print the input files
# echo -e "\ninput example.txt:"
# hdfs dfs -cat input/example.txt

# print the output of wordcount
echo -e "\nwordcount output:"
hdfs dfs -cat output/part-00000

