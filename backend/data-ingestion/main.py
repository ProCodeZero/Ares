from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Модель данных для GPS
class GPSData(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    speed: int
    timestamp: str

# Подключение к Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/ingest/gps")
async def ingest_gps(data: GPSData):
    producer.send("gps_topic", data.dict())
    return {"status": "success"}