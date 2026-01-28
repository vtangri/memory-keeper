import redis
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages caching for frequent queries using Redis.
    """
    
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            self.redis = redis.from_url(redis_url)
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self.redis = None

    def get(self, key: str):
        if not self.redis: return None
        val = self.redis.get(key)
        if val:
            return json.loads(val)
        return None

    def set(self, key: str, value: dict, expire: int = 3600):
        if not self.redis: return
        self.redis.setex(key, expire, json.dumps(value))

    def invalidate(self, key_pattern: str):
        # advanced logic for pattern matching deletion
        pass
