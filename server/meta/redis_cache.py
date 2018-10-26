import functools
import json

from server.database import redis_cache_conn
from server.utils.gen_fp import gen_request_fp, gen_special_fp


def redis_cache(expire_time=1800, **special_params):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if special_params:
                fp = gen_special_fp(special_params)
            else:
                fp = gen_request_fp()
            result = redis_cache_conn.get(fp)
            if result:
                print("=" * 50, "Using Cache")
                result = json.loads(result)
                if len(result) == 2:
                    return result[0], result[1]
                return result
            print("=" * 50, "NOT Using Cache")
            result = func(*args, **kwargs)
            redis_cache_conn.set(fp, json.dumps(result), expire_time)
            return result
        return wrapped_func
    return decorator
