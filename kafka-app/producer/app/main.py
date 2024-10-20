import random
from fastapi import FastAPI
from pydantic import BaseModel
from kafka_client import KafkaClient

app = FastAPI()

class Message(BaseModel):
    content: str


@app.post("/produce")
async def produce_message(message: Message):
    key = str(random.randint(1, 3))
    print(key)
    return KafkaClient().publish_message(message.content, key=key)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)