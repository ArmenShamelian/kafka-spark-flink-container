import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import Slide

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env_settings = (
    EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
)
st_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

# Define source
st_env.execute_sql(
    f"""
    CREATE TABLE source (
        id INT,
        name STRING,
        age INT,
        ts BIGINT,
        rowtime as TO_TIMESTAMP(FROM_UNIXTIME(ts, 'yyyy-MM-dd HH:mm:ss')),
        WATERMARK FOR rowtime AS rowtime - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka-0.11',
        'topic' = '{os.environ["KAFKA_TOPIC"]}',
        'scan.startup.mode' = 'latest-offset',
        'properties.bootstrap.servers' = '{os.environ["KAFKA_HOST"]}',
        'properties.zookeeper.connect' = '{os.environ["ZOOKEEPER_HOST"]}',
        'properties.group.id' = '{os.environ["KAFKA_CONSUMER_GROUP"]}',
        'format' = 'json'
    )
    """
)

# Define output sink
st_env.execute_sql(
    """
    CREATE TABLE sink (
        average_age DOUBLE,
        window_end TIMESTAMP(3)
    ) WITH (
        'connector' = 'print',
        'print-identifier' = 'Average Age, Window: '
    )
"""
)

st_env.from_path("source").window(
    Slide.over("10.seconds").every("3.seconds").on("rowtime").alias("w")
).group_by("w").select(
    "AVG(1.0 * age) as average_age, w.end AS window_end"
).insert_into(
    "sink"
)

st_env.execute("PyFlink job")
