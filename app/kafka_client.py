from concurrent.futures import Future
from enum import Enum
import os
from confluent_kafka import Producer
from pydantic import BaseModel


class KafkaClientException(Exception):
    pass

class KafkaClientStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"


class KafkaClientResult(BaseModel):
    status: KafkaClientStatus
    message: str


class KafkaClient:
    def __init__(self):
        self.create_producer()

    def create_producer(self):
        self.producer = Producer({
            'bootstrap.servers': os.environ.get(
                'KAFKA_BOOTSTRAP_SERVERS',
                'kafka-demo-kafka-1:9092'
            )
        })

    def publish_message(self, topic: str, message: str) -> KafkaClientResult:
        try:
            if not self.producer:
                self.create_producer()

            future = Future()
            def delivery_callback(err, msg):
                if err:
                    raise KafkaClientException(err)
                else:
                    future.set_result(msg)

            self.producer.produce(topic, message, callback=delivery_callback)
        
            remaining_messages = self.producer.flush(timeout=5)
            if remaining_messages > 0:
                print(f"Failed to deliver {remaining_messages} messages")

            kafka_message = future.result(timeout=5)
            message = f"Message delivered to topic {kafka_message.topic()} [{kafka_message.partition()}] at offset {kafka_message.offset()}"
            return KafkaClientResult(status=KafkaClientStatus.SUCCESS, message=message)
        except KafkaClientException as e:
            return KafkaClientResult(status=KafkaClientStatus.FAILED, message=str(e))