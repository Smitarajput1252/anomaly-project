from kafka import KafkaConsumer
import json
from config import KAFKA_SERVER, KAFKA_TOPIC
from utils.gemini_analyzer import analyze_vitals
from database.db import insert_data, create_table

create_table()

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for message in consumer:
    vitals = message.value
    result = analyze_vitals(vitals)

    severity = result["severity"]
    reason = result["reason"]

    insert_data(vitals, severity, reason)
    print("Stored:", severity)