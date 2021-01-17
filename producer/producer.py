import time
import os
import csv
import json
from datetime import datetime, timezone
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=[os.environ["KAFKA_HOST"]],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    api_version=(0, 11),
)

while True:
    with open(os.environ["DATA"], "r") as file:
        reader = csv.reader(file, delimiter=",")
        headers = next(reader)
        for row in reader:
            value = {headers[i]: row[i] for i in range(len(headers))}
            value["ts"] = int(time.time())
            producer.send(os.environ["KAFKA_TOPIC"], value=value)
            time.sleep(float(os.environ["KAFKA_INTERVAL"]))
