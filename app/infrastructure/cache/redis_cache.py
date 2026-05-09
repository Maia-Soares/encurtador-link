import json
import redis
from typing import Any, Optional
from redis.cluster import logger
from app.domain.cache import CacheInterface


class RedisCacheAdapter(CacheInterface):
    def __init__(self, redis_client: redis.Redis, ttl_seconds: int = 3600):
        self.client = redis_client
        self.default_ttl = ttl_seconds

    def get(self, key: str) -> Optional[dict[str, Any]]:
        try:
            data = self.client.get(key)
            if data is None:
                return None
            parsed = json.loads(data)
            if parsed.get("expires_at"):
                from datetime import datetime

                parsed["expires_at"] = datetime.fromisoformat(parsed["expires_at"])
            if parsed.get("last_accessed"):
                from datetime import datetime

                parsed["last_accessed"] = datetime.fromisoformat(
                    parsed["last_accessed"]
                )
            if parsed.get("created_at"):
                from datetime import datetime

                parsed["created_at"] = datetime.fromisoformat(parsed["created_at"])
            return parsed
        except Exception as e:
            logger.warning(f"Redis get failed: {e}. Falling back to DB-only.")
            return None

    def set(self, key: str, value: dict[str, Any], ttl_seconds: int = None) -> None:
        try:
            safe_value = {
                k: v.isoformat() if hasattr(v, "isoformat") else v
                for k, v in value.items()
            }
            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
            self.client.setex(key, ttl, json.dumps(safe_value))
        except Exception as e:
            logger.warning(f"Redis set failed: {e}. Continuing without cache.")

    def delete(self, key: str) -> None:
        try:
            self.client.delete(key)
        except Exception as e:
            logger.warning(f"Redis delete failed: {e}. Continuing.")
