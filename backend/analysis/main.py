import json
import uuid
import logging
import asyncio
from datetime import datetime
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from anomaly_rules import detect_speed_anomaly, detect_geofence_anomaly

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# PostgreSQL
engine = create_engine("postgresql://postgres:root@postgres:5432/ares_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True)
    device_id = Column(String)
    anomaly_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)

Base.metadata.create_all(engine)

async def consume_messages():
    consumer = AIOKafkaConsumer(
        'gps_topic',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            if detect_speed_anomaly(data['speed']):
                save_incident(data, "speed_anomaly")
            if detect_geofence_anomaly(data['latitude'], data['longitude']):
                save_incident(data, "geofence_anomaly")
    finally:
        await consumer.stop()

def save_incident(data, anomaly_type):
    with Session() as session:
        incident = Incident(
            id=str(uuid.uuid4()),
            device_id=data['device_id'],
            anomaly_type=anomaly_type,
            latitude=data['latitude'],
            longitude=data['longitude'],
            timestamp=datetime.utcnow()
        )
        session.add(incident)
        try:
            session.commit()
            logging.info(f"Incident saved: {incident.id}")
        except Exception as e:
            session.rollback()
            logging.error(f"Failed to save incident: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())