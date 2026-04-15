import redis.asyncio as redis
from WebStreamer.vars import Var

redis_client = redis.from_url(Var.REDIS_URL, decode_responses=True)

async def increment_workload(client_index: int):
    try:
        await redis_client.hincrby("hydrostreamer:workloads", str(client_index), 1)
    except Exception:
        pass

async def decrement_workload(client_index: int):
    try:
        await redis_client.hincrby("hydrostreamer:workloads", str(client_index), -1)
    except Exception:
        pass

async def get_fastest_client() -> int:
    try:
        workloads = await redis_client.hgetall("hydrostreamer:workloads")
        if not workloads:
            return 0
        workloads_int = {int(k): int(v) for k, v in workloads.items()}
        return min(workloads_int, key=workloads_int.get)
    except Exception:
        return 0
