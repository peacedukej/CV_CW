import redis

redis_client = redis.Redis(host='redis_server', port=6379, decode_responses=True)
