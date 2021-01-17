import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, from_json, window

spark = SparkSession.builder.appName("AverageAge").getOrCreate()

# Get rid of INFO and WARN logs.
spark.sparkContext.setLogLevel("ERROR")

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", os.environ["KAFKA_HOST"])
    .option("subscribe", os.environ["KAFKA_TOPIC"])
    .option("startingOffsets", "latest")
    .option("groupIdPrefix", os.environ["KAFKA_CONSUMER_GROUP"])
    .load()
)

schema = StructType(
    [
        StructField("id", StringType()),
        StructField("name", StringType()),
        StructField("age", StringType()),
    ]
)

# Parse the "value" field as JSON format.
parsed_values = df.select(
    "timestamp", from_json(col("value").cast("string"), schema).alias("parsed_values")
)
# We only need the Age column for now.
ages = parsed_values.selectExpr("timestamp", "parsed_values.age AS age")

# We set a window size of 10 seconds, sliding every 5 seconds.
averageAge = ages.groupBy(window(ages.timestamp, "10 seconds", "5 seconds")).agg(
    {"age": "avg"}
)

query = (
    averageAge.writeStream.outputMode("update")
    .queryName("average_age")
    .format("console")
    .trigger(processingTime="1 seconds")
    .option("truncate", "false")
    .start()
    .awaitTermination()
)
