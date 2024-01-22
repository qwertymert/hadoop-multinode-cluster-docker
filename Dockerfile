FROM ubuntu:20.04
ENV TZ=Europe/Istanbul 
ARG DEBIAN_FRONTEND=noninteractive

MAINTAINER qwertymert <gulsen20@itu.edu.tr>

WORKDIR /root

# install openssh-server, openjdk and wget
RUN apt-get update && apt-get install -y openssh-server openjdk-11-jdk wget python3 python3-pip nano

RUN pip install mrjob

# install hadoop 3.3.6
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzvf hadoop-3.3.6.tar.gz && \
    mv hadoop-3.3.6 /usr/local/hadoop && \
    rm hadoop-3.3.6.tar.gz

# set environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 
ENV HADOOP_HOME=/usr/local/hadoop 
ENV PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin 

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

RUN mkdir -p ~/hdfs/namenode && \ 
    mkdir -p ~/hdfs/datanode && \
    mkdir $HADOOP_HOME/logs && \
    mkdir -p ~/data

COPY config/* /tmp/

RUN mv /tmp/ssh_config ~/.ssh/config && \
    mv /tmp/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh && \
    mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \ 
    mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    mv /tmp/workers $HADOOP_HOME/etc/hadoop/workers && \
    mv /tmp/start-hadoop.sh ~/start-hadoop.sh && \
    mv /tmp/run-wordcount.sh ~/run-wordcount.sh && \
    mv /tmp/stop-hadoop.sh ~/stop-hadoop.sh && \
    mv /tmp/run-python-example.sh ~/run-python-example.sh && \
    mv /tmp/mapper.py ~/mapper.py && \
    mv /tmp/reducer.py ~/reducer.py && \
    mv /tmp/example.txt ~/example.txt && \
    mv /tmp/decision_tree.py ~/decision_tree.py

RUN chmod +x ~/start-hadoop.sh && \
    chmod +x ~/run-wordcount.sh && \
    chmod +x ~/run-python-example.sh && \
    chmod +x ~/mapper.py && \
    chmod +x ~/reducer.py && \
    chmod +x ~/decision_tree.py && \
    chmod +x $HADOOP_HOME/sbin/start-all.sh && \
    chmod +x ~/stop-hadoop.sh && \
    chmod +x $HADOOP_HOME/sbin/stop-all.sh

# format namenode
RUN /usr/local/hadoop/bin/hdfs namenode -format

CMD [ "sh", "-c", "service ssh start; bash"]

EXPOSE 8088

