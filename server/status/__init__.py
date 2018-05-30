# coding=utf-8
# author=veficos


class HTTPStatus:
    # 成功
    Ok = 200

    # 参数错误
    BadRequest = 400

    # 验证失败
    UnAuthorized = 401

    # 服务器拒绝该请求
    Forbidden = 403

    # 未找到该资源
    NotFound = 404

    # 服务器内部错误
    InternalServerError = 500

    # 服务器超载
    ServiceUnavailable = 503

    # 用户未认证
    UserAuthError = 400001

    # 货源下架
    GoodCloseError = 400003


class APIStatus:
    # 成功
    Ok = 100000

    # 请求参数有误
    BadRequest = 100001

    # 服务器内部有误
    InternalServerError = 100002

    # 服务器拒绝此请求
    Forbidden = 100003

    # 没有此用户
    NotUser = 100004

    # 密码错误
    PasswdError = 100005

    # 用户未登录
    UnLogin = 100006

    # 未找到资源
    NotFound = 100404

    # 用户未认证
    UserAuthError = 400001

    # 货源下架
    GoodCloseError = 400003


class FeedAPIStatus(APIStatus):
    TimeFormatError = 102001
    GoodsNameFormatError = 102002
    GoodsWeightFormatError = 102003
    GoodsVolumeFormatError = 102004
    GoodsPriceExpectFormatError = 102005
    GoodsDescriptionFormatError = 102006
    GoodsSameAddress = 102007
    GoodsRequestVehicle = 102008
    GoodsUnknownCarpoolType = 102009
    Decriptions = {
        APIStatus.Ok: '成功',
        APIStatus.NotFound: '未找到该资源',
        APIStatus.BadRequest: '请求参数有误',
        APIStatus.InternalServerError: '服务器内部错误',
        APIStatus.UnLogin: '未登录用户',
        APIStatus.Forbidden: '拒绝该请求',
        TimeFormatError: '时间格式错误',
        GoodsNameFormatError: '货物名至少需要两个字',
        GoodsWeightFormatError: '货源重量格式错误',
        GoodsVolumeFormatError: '货源体积格式错误',
        GoodsPriceExpectFormatError: '货源期望价格格式错误',
        GoodsDescriptionFormatError: '给司机捎句话最多五十个字',
        GoodsSameAddress: '货源的出发地和目的地相同',
        GoodsRequestVehicle: '车长与车型填写错误',
        GoodsUnknownCarpoolType: '拼单类型错误',

    }


class UserAPIStatus(APIStatus):
    Decriptions = {
        APIStatus.Ok: '成功',
        APIStatus.NotFound: '未找到该资源',
        APIStatus.BadRequest: '请求参数有误'
    }


def to_http_status(status):
    return {
        APIStatus.Ok: HTTPStatus.Ok,
        APIStatus.InternalServerError: HTTPStatus.InternalServerError,
        APIStatus.Forbidden: HTTPStatus.Forbidden,
        APIStatus.NotUser: HTTPStatus.Forbidden,
        APIStatus.PasswdError: HTTPStatus.Forbidden,
        APIStatus.UnLogin: HTTPStatus.Forbidden,
        APIStatus.NotFound: HTTPStatus.NotFound,

        FeedAPIStatus.BadRequest: HTTPStatus.BadRequest,
        FeedAPIStatus.TimeFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsNameFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsWeightFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsVolumeFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsPriceExpectFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsDescriptionFormatError: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsSameAddress: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsRequestVehicle: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodsUnknownCarpoolType: HTTPStatus.BadRequest,
        FeedAPIStatus.GoodCloseError: HTTPStatus.BadRequest,
    }[status]


Decriptions = {
    APIStatus.Ok: '成功',
    APIStatus.NotFound: '未找到该资源',
    APIStatus.BadRequest: '请求参数有误',
    APIStatus.InternalServerError: '服务器内部错误',
    APIStatus.UnLogin: '未登录用户',
    APIStatus.Forbidden: '拒绝该请求',

    FeedAPIStatus.TimeFormatError: '时间格式错误',
    FeedAPIStatus.GoodsNameFormatError: '货物名至少需要两个字',
    FeedAPIStatus.GoodsWeightFormatError: '货源重量格式错误',
    FeedAPIStatus.GoodsVolumeFormatError: '货源体积格式错误',
    FeedAPIStatus.GoodsPriceExpectFormatError: '货源期望价格格式错误',
    FeedAPIStatus.GoodsDescriptionFormatError: '给司机捎句话最多五十个字',
    FeedAPIStatus.GoodsSameAddress: '货源的出发地和目的地相同',
    FeedAPIStatus.GoodsRequestVehicle: '车长与车型填写错误',
    FeedAPIStatus.GoodsUnknownCarpoolType: '拼单类型错误',
    FeedAPIStatus.GoodCloseError: '货源已被其它司机抢了',
}


def build_result(status, msg=None, count=None, data=None):
    if data:
        return {'status': status, 'msg': msg if msg else Decriptions[status], 'count': count if count else None,
                'data': data}
    return {'status': status, 'msg': msg if msg else Decriptions[status]}


def make_result(status, msg=None, data=None):
    return {'status': status, 'msg': msg if msg else Decriptions[status], 'data': data}
