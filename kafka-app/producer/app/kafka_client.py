from concurrent.futures import Future
from enum import Enum
import os
from confluent_kafka import Producer
from pydantic import BaseModel
from config import get_settings


class KafkaClientException(Exception):
    pass


class KafkaClientStatus(Enum):
    SUCCESS = "Success"


class KafkaClientResult(BaseModel):
    status: KafkaClientStatus
    message: str


class KafkaClient:
    def __init__(self):
        self.settings = get_settings()
        self.__create_producer()

    def __create_producer(self):
        self.producer = Producer({
            'bootstrap.servers': self.settings.kafka_bootstrap_servers,
            'delivery.timeout.ms': self.settings.delivery_timeout_ms,
            'acks': self.settings.acks,
            'enable.idempotence': self.settings.enable_idempotence,
            'retries': self.settings.retries,
            'retry.backoff.ms': self.settings.retry_backoff_ms,
            'compression.type': self.settings.compression_type,
            'client.id': self.settings.client_id,
        })

    def publish_message(self, message: str, key: str) -> KafkaClientResult:
        future = Future()
        def delivery_callback(err, msg):
            if err:
                future.set_exception(KafkaClientException(err))
            else:
                future.set_result(msg)
        self.producer.produce(self.settings.topic, message, key=key, callback=delivery_callback)
    
        remaining_messages = self.producer.flush(timeout=5)
        if remaining_messages > 0:
            print(f"Failed to deliver {remaining_messages} messages")

        kafka_message = future.result(timeout=5)
        message = f"Message delivered to topic {kafka_message.topic()} [{kafka_message.partition()}] at offset {kafka_message.offset()}"
        return KafkaClientResult(status=KafkaClientStatus.SUCCESS, message=message)    
