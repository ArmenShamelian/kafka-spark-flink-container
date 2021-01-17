FROM flink:1.11.2-scala_2.11
WORKDIR /
RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip python3.7-dev && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN pip3 install apache-flink==1.11.2
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka-0.11_2.11/1.11.2/flink-sql-connector-kafka-0.11_2.11-1.11.2.jar;
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/1.11.2/flink-json-1.11.2.jar;
COPY . .
CMD python -u $SCRIPT