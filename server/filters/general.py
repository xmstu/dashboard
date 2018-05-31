import json

from server.meta.decorators import make_decorator, Response
from server.utils.extend import ExtendHandler


class General(object):
    @staticmethod
    @make_decorator
    def success(data):
        data = json.loads(json.dumps(data, default=ExtendHandler.handler))
        return Response(data=data)
