import functools
import json

from server.database import redis_cache_conn
from server.utils.gen_fp import gen_fp


def redis_cache(expire_time=1800):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            fp = gen_fp()
            result = redis_cache_conn.get(fp)
            if result:
                result = json.loads(result)
                # print("=" * 50, "Using Cache")
                return result[0], result[1]
            result = func(*args, **kwargs)
            redis_cache_conn.set(fp, json.dumps(result), expire_time)
            # print("=" * 50, "Not Using Cache")
            return result
        return wrapped_func
    return decorator
