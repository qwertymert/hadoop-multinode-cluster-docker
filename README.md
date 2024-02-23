# How To Run

Note: This guide is for Linux (Ubuntu) machines, however, commands can be adapted for other operating systems or a virtual environment can be used instead. (Example: WSL)

-- Steps for running --

First, setup Docker to your computer.

Open a terminal inside the hadoop-docker-latest folder.

Run build-image.sh to build Docker image.
```
. build-image.sh
```

Run following command to create a bridge Network for connecting nodes.

```
. sudo docker network create --driver=bridge hadoop
```

Run start-container to start master and worker node containers and open master node terminal. By default, 2 DataNodes are started.

```
. start-container.sh
```

After opening the master node terminal, run start-hadoop.sh to start hadoop services (HDFS, YARN). You can view web interface of Hadoop at the url "http://localhost:8088/"

```
. start-hadoop.sh
```

Run example Java MapReduce word count task after starting hadoop. Results are displayed on the terminal.

```
. run-wordcount.sh
```

To run example Python task after Java example, input and output directories should be deleted in HDFS to run an example again.

List folders in HDFS
```
hdfs dfs -ls
```

Delete input folder
```
hdfs dfs -rm -r input 
```
Delete output folder
```
hdfs dfs -rm -r output 
```

Run python example
```
. run-python-example.sh
```

To stop hadoop and close docker containers run following commands
```
. stop-hadoop.sh
exit
```

-- Example usage to put csv file to HDFS

Download the data from [here](https://www.kaggle.com/datasets/mryanm/luflow-network-intrusion-detection-data-set/data) and extract it to the `data` folder.

Run the python code data_process.py to merge multiple files into one file and apply required preprocessing.

Upload the merged.csv file to HDFS using the following command:

```
hdfs dfs -put merged.csv "your_location_here"
```