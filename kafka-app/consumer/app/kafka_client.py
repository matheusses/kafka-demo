from aiokafka import AIOKafkaConsumer
import asyncio
from config import get_settings

class KafkaClient:
    def __init__(self):
        self.settings = get_settings()
        self.__create_consumer()

    def __create_consumer(self):
        self.consumer = AIOKafkaConsumer(
            self.settings.topics,
            bootstrap_servers=self.settings.kafka_bootstrap_servers,
            client_id=self.settings.client_id,
            group_id=self.settings.group_id,
            auto_offset_reset=self.settings.auto_offset_reset,
        )

    async def consume_message(self):

        await self.consumer.start()
        try:
            async for message in self.consumer:
                print(f"Received message:")
                print(f"  Topic: {message.topic}")
                print(f"  Partition: {message.partition}")
                print(f"  Offset: {message.offset}")
                print(f"  Key: {message.key.decode('utf-8') if message.key else 'None'}")
                print(f"  Value: {message.value.decode('utf-8')}")
                print("--------------------")
        except asyncio.CancelledError:
            print("Stopping consumer...")
        finally:
            await self.consumer.stop()
