import json
import time
import os
import redis


class MetricsCollector:
    def __init__(self):
        self.redis_client = redis.from_url(
            os.getenv("REDIS_URL"),
            decode_responses=True
        )

    def store_request(self, data: dict):
        data["timestamp"] = time.time()
        self.redis_client.lpush("autopilot:requests", json.dumps(data))

    def store_guardrail_violation(self, query: str, violation: str):
        payload = {"query": query, "violation": violation, "timestamp": time.time()}
        self.redis_client.lpush("autopilot:guardrails", json.dumps(payload))

    def get_recent_requests(self, limit: int = 50):
        logs = self.redis_client.lrange("autopilot:requests", 0, limit - 1)
        return [json.loads(log) for log in logs]

    def get_guardrail_logs(self, limit: int = 50):
        logs = self.redis_client.lrange("autopilot:guardrails", 0, limit - 1)
        return [json.loads(log) for log in logs]
