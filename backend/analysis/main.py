import json
import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, WebSocket
from aiokafka import AIOKafkaConsumer
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
from anomaly_rules import detect_speed_anomaly, detect_geofence_anomaly

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# WebSocket connections pool
connected_clients: List[WebSocket] = []

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

@app.get("/api/incidents", response_model=List[dict])
async def get_all_incidents():
    with Session() as session:
        incidents = session.query(Incident).all()
        return [
            {
                "id": incident.id,
                "device_id": incident.device_id,
                "anomaly_type": incident.anomaly_type,
                "latitude": incident.latitude,
                "longitude": incident.longitude,
                "timestamp": incident.timestamp.isoformat()
            }
            for incident in incidents
        ]

# WebSocket endpoint
@app.websocket("/ws/incidents")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        connected_clients.remove(websocket)

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
            incident_data = process_anomaly(data)
            if incident_data:
                await notify_clients(incident_data)
    finally:
        await consumer.stop()

def process_anomaly(data: dict):
    incident_data = None
    if detect_speed_anomaly(data['speed']):
        incident_data = save_incident(data, "speed_anomaly")
    elif detect_geofence_anomaly(data['latitude'], data['longitude']):
        incident_data = save_incident(data, "geofence_anomaly")
    return incident_data  # Теперь это словарь

def save_incident(data: dict, anomaly_type: str):
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
        session.commit()
        incident_data = {
            "id": incident.id,
            "device_id": incident.device_id,
            "anomaly_type": anomaly_type,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "timestamp": incident.timestamp.isoformat()
        }
        return incident_data

async def notify_clients(incident_data: dict):  # Теперь принимаем словарь
    for client in connected_clients:
        await client.send_json(incident_data)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())