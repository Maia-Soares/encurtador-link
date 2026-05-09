import redis
from app.core.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_cache_ttl() -> int:
    return settings.CACHE_TTL_SECONDS
