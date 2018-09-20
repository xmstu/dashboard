from flask_restful import abort

from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus


def get_role_regions(region_id):
    role_type, locations_id = SessionOperationClass.get_locations()
    if 1 == role_type:
        if not region_id:
            region_id = 0
    elif 2 == role_type or 3 == role_type or 4 == role_type:
        if not region_id:
            region_id = locations_id
        else:
            if str(region_id) not in locations_id:
                abort(HTTPStatus.Forbidden, **make_result(status=APIStatus.Forbidden, msg='非权限范围内地区'))
    else:
        abort(HTTPStatus.Forbidden, **make_result(status=APIStatus.Forbidden, msg='非权限角色在进行操作'))

    return region_id
