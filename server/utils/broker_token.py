# -*- coding: utf-8 -*-

import json
import base64
import hashlib
import datetime
from urllib.parse import quote, unquote
from server.status import HTTPStatus, make_resp, APIStatus
from flask_restful import abort

headers = b'{"alg":"HS256","typ":"JWT"}'
datetime_fields = ['exp']
secret_key = "3xm7l#p+r-tadmg*03^js3@ke_uznn$2^^vxfkr3&wxmsz!&i0"

def to_utc_timestamp(x):
    """datetime转时间戳"""
    return x.timestamp() if x else None

def from_utc_timestamp(utc_timestamp):
    """时间戳转datetime"""
    return datetime.datetime.fromtimestamp(utc_timestamp)

def encrypt(password, key):
    """sha256加密"""
    return hashlib.pbkdf2_hmac('sha256', password, key, 100000)

def encode(payload):
    """token加密"""
    for k in datetime_fields:
        v = payload.get(k)
        if isinstance(v, datetime.datetime):
            payload[k] = to_utc_timestamp(v)
    segments = []
    payload = json.dumps(payload, separators=(',', ':')).encode()
    segments.append(base64.standard_b64encode(headers))
    segments.append(base64.standard_b64encode(payload))
    signature = encrypt(b'.'.join(segments), secret_key.encode())
    segments.append(base64.standard_b64encode(signature))
    token = b'.'.join(segments).decode()
    return quote(token, safe='')


def decode(token, datatime_format=False):
    """token解密"""
    token = unquote(token)
    segments = token.split('.')
    if len(segments) != 3:
        abort(HTTPStatus.UnAuthorized, **make_resp(status=APIStatus.UnLogin, msg='token验证失败'))
    segments = [s.encode() for s in segments]
    signature_origin = segments.pop()
    signature = encrypt(b'.'.join(segments), secret_key.encode())
    signature = base64.standard_b64encode(signature)
    if signature != signature_origin:
        abort(HTTPStatus.UnAuthorized, **make_resp(status=APIStatus.UnLogin, msg='token验证失败'))
    try:
        payload = json.loads(base64.standard_b64decode(segments[1]).decode())
    except:
        abort(HTTPStatus.UnAuthorized, **make_resp(status=APIStatus.UnLogin, msg='token验证失败'))
        raise
    if not datatime_format:
        return payload
    for k in datetime_fields:
        if k in payload:
            payload[k] = from_utc_timestamp(payload[k])
    return payload


if __name__ == '__main__':
    token1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjkwNSwidHkiOjIsIm1vYmlsZSI6IjEzODA5NjkzNDU4IiwiZXhwIjoxNTM2NzE2MzgzfQ%3D%3D.BCaspRnzwcVnaKaGyR0zY0BpYDEK9QkJwKInQNiBajk%3D'
    payload = decode(token1)
    print(payload)