import hashlib
import re

import w3lib.url
from flask import session
from flask_restful import request

from server.utils.request import get_payload


def utf8_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return string.encode('utf-8')


# 生成请求指纹
def gen_fp():
    # url排序
    url = re.sub("&_=(\d+)", "", request.url)
    url = w3lib.url.canonicalize_url(url)

    method = request.method.upper()

    if method == "GET":
        params = request.args.to_dict() if request.args.to_dict() else {}
        if params:
            try:
                params.pop("_")
            except Exception:
                pass

    elif method == "POST":
        params = get_payload()
    else:
        params = {}

    params = str(sorted(params.items()))

    # 获取用户名和用户角色作为唯一标识
    user_name = session['login'].get('user_name', '')
    role = session['login'].get('role', '')

    temp_str = url + method + params + user_name + role

    sha1 = hashlib.sha1()

    sha1.update(utf8_string(temp_str))

    fp = sha1.hexdigest()

    return fp
