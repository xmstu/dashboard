import functools
import json

from server.database import redis_cache_conn
from server.status import make_resp, APIStatus, HTTPStatus
from server.utils.gen_fp import gen_fp


def redis_cache(expire_time=1800):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            fp = gen_fp()
            result = redis_cache_conn.get(fp)
            if result:
                print("=" * 50, "Using Cache")
                result = json.loads(result)
                return make_resp(APIStatus.Ok, count=result[0].get("count", 0), data=result[0].get("data", [])), HTTPStatus.Ok
            result = func(*args, **kwargs)
            print("=" * 50, "Not Using Cache")
            redis_cache_conn.set(fp, json.dumps(result), expire_time)
            return result
        return wrapped_func
    return decorator
