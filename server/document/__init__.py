# coding=utf-8


from flask_restplus import fields
from server.status import FeedAPIStatus
from server.app import api


response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(FeedAPIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.Ok]),
}))

response_bad_request = api.response(400, '请求参数错误', api.model('response_bad_request', {
    'state': fields.Integer(description=str(FeedAPIStatus.BadRequest)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.BadRequest]),
}))

response_unauthorized = api.response(401, '验证失败', api.model('response_unauthorized', {
    'state': fields.Integer(description=str(FeedAPIStatus.UnLogin)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.UnLogin]),
}))

response_forbidden = api.response(403, '服务器拒绝该请求', api.model('response_response_forbidden', {
    'state': fields.Integer(description=str(FeedAPIStatus.Forbidden)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.Forbidden]),
}))

response_not_found = api.response(404, '未找到货源', api.model('response_not_found', {
    'state': fields.Integer(description=str(FeedAPIStatus.NotFound)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.NotFound]),
}))

response_internal_server_error = api.response(500, '内部服务器错误', api.model('response_internal_server_error', {
    'state': fields.Integer(description=str(FeedAPIStatus.InternalServerError)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[FeedAPIStatus.InternalServerError]),
}))