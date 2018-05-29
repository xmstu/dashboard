import json

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus


class UserList(object):

    @staticmethod
    @make_decorator
    def get(user_list):
        # 过滤字段
        user_list = json.loads(json.dumps(user_list))
        user_detail = user_list['user_detail']
        for detail in user_detail:
            # 认证
            role_auth = []
            if detail['auth_goods']:
                role_auth.append('货主')
            if detail['auth_driver']:
                role_auth.append('司机')
            if detail['auth_company']:
                role_auth.append('物流公司')
            detail['role_auth'] = ','.join(role_auth) if role_auth else '未认证'
            detail.pop('auth_goods')
            detail.pop('auth_driver')
            detail.pop('auth_company')

            detail['usual_city'] = detail['usual_city'] if detail['usual_city'] else ''

        return build_result(APIStatus.Ok, data={'list': user_detail, 'counts': user_list['user_count']}), HTTPStatus.Ok