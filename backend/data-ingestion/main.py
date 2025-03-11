from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json

app = FastAPI()

# Модель входных данных
class GPSData(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: str

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post('/ingest/gps')
async def ingest_gps(data: GPSData):
    producer.send("gps_data", data.model_dump())
    return {"status": "Data sent to Kafka"}