from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result


class Paging(object):
    @staticmethod
    @make_decorator
    def check_paging(page, limit, **kwargs):
        # 检验page, limit是否为整数
        if not str(page).isdigit() or int(page) <= 0:
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='page参数不能为%s' % page))

        if not str(limit).isdigit() or (int(limit) not in [10, 20, 30, 40, 50, 300]):
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='count参数不能为%s' % limit))

        log.info("params:{}".format(kwargs))
        return Response(page=int(page), limit=int(limit), **kwargs)
