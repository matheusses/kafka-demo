from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from kafka_client import KafkaClient

app = FastAPI()

# Simulating a message queue
message_queue = asyncio.Queue()

class Message(BaseModel):
    content: str


@app.post("/produce")
async def produce_message(message: Message):
    return KafkaClient().publish_message("teste", message.content)
    

@app.get("/consume")
async def consume_message():
    if message_queue.empty():
        return {"message": "No messages available"}
    message = await message_queue.get()
    return {"message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)