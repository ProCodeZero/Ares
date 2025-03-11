from fastapi import FastAPI
from kafka import KafkaConsumer
import pandas as pd
import json

app = FastAPI()

# Kafka consumer
consumer = KafkaConsumer(
    'gps_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def detect_anomaly(data):
    # Пример: обнаружение аномальной скорости
    return data['speed'] > 100

@app.on_event("startup")
async def process_data():
    for message in consumer:
        data = message.value
        if detect_anomaly(data):
            print(f"Аномалия обнаружена: {data}")