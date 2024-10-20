from fastapi import FastAPI, BackgroundTasks
import asyncio
import json
from contextlib import asynccontextmanager

from kafka_client import KafkaClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consume())
    yield

app = FastAPI(lifespan=lifespan)

async def consume():
    await KafkaClient().consume_message()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
