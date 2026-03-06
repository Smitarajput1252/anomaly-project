from kafka import KafkaProducer
import json, time, random
from config import KAFKA_SERVER, KAFKA_TOPIC

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    vitals = {
        "heart_rate": random.randint(55, 160),
        "spo2": random.randint(82, 100),
        "temperature": round(random.uniform(35.5, 40), 1),
        "bp_systolic": random.randint(95, 180)
    }

    producer.send(KAFKA_TOPIC, vitals)
    print("Sent:", vitals)
    time.sleep(3)