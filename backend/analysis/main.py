from fastapi import FastAPI
from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Подключение к Kafka
consumer = KafkaConsumer(
    'gps_topic',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Подключение к PostgreSQL
engine = create_engine("postgresql://postgres:root@postgres:5432/ares_db")
Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True)
    device_id = Column(String)
    anomaly_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Правила обнаружения аномалий
def detect_speed_anomaly(data):
    return data['speed'] > 100  # Пример: превышение скорости

def detect_geofence_anomaly(data):
    # Пример: выход за геозону (широта > 56)
    return data['latitude'] > 56.0

@app.on_event("startup")
async def process_data():
    for message in consumer:
        data = message.value
        # Проверка аномалий
        if detect_speed_anomaly(data):
            save_incident(data, "speed_anomaly")
        if detect_geofence_anomaly(data):
            save_incident(data, "geofence_anomaly")

def save_incident(data, anomaly_type):
    session = Session()
    incident = Incident(
        id=data['device_id'] + "_" + str(datetime.utcnow()),
        device_id=data['device_id'],
        anomaly_type=anomaly_type,
        latitude=data['latitude'],
        longitude=data['longitude'],
        timestamp=datetime.utcnow()
    )
    session.add(incident)
    session.commit()
    session.close()