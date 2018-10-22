import hashlib
import re

import six
import w3lib.url
from flask import session
from flask_restful import request


def utf8_string(string):
    if six.PY2:
        if isinstance(string, str):
            return string
        else:
            return string.encode('utf-8')
    elif six.PY3:
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

    params = request.args.to_dict() if request.args.to_dict() else {}
    if params:
        params.pop("_")

    params = str(sorted(params.items()))

    data = request.data if request.data else {}
    data = str(sorted(data.items()))

    # 获取用户名和用户角色作为唯一标识
    user_name = session['login'].get('user_name', '')
    role = session['login'].get('role', '')

    temp_str = url + method + params + data + user_name + role

    sha1 = hashlib.sha1()

    sha1.update(utf8_string(temp_str))

    fp = sha1.hexdigest()

    return fp
