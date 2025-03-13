from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'gps_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

for message in consumer:
    print(message.value)