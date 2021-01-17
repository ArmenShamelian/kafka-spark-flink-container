FROM jupyter/pyspark-notebook:703d8b2dcb88
WORKDIR /
RUN pip install pyspark==3.0.1
COPY . .
CMD spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 $SCRIPT