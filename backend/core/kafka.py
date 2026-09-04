import json
import asyncio
import logging
from backend.core.config import settings

logger = logging.getLogger(__name__)

class KafkaPublisher:
    def __init__(self):
        self.producer = None
        self.topic = settings.KAFKA_TOPIC_METADATA
        self.is_connected = False
        self.local_handlers = []

    def subscribe_local(self, handler):
        """Register a local handler for fallback in-memory mode."""
        self.local_handlers.append(handler)

    async def start(self):
        try:
            from aiokafka import AIOKafkaProducer
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BROKER_URL,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=1500
            )
            await self.producer.start()
            self.is_connected = True
            logger.info(f"Connected to Kafka broker at {settings.KAFKA_BROKER_URL}")
        except Exception as e:
            self.is_connected = False
            logger.warning(f"Kafka broker unavailable ({e}). Using in-memory event spine.")

    async def stop(self):
        if self.producer and self.is_connected:
            try:
                await self.producer.stop()
            except Exception:
                pass

    async def publish_sighting(self, data: dict):
        if self.is_connected and self.producer:
            try:
                await self.producer.send_and_wait(self.topic, data)
                return
            except Exception as e:
                logger.warning(f"Kafka send failed: {e}. Falling back to in-memory dispatch.")
        
        # Dispatch to local handlers (CorrelationEngine)
        for handler in self.local_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as ex:
                logger.error(f"Error executing local event handler: {ex}")

# Singleton instance
publisher = KafkaPublisher()
