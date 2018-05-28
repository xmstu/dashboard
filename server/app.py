# -*- coding: utf-8 -*-

from flask import Flask, jsonify, session, request, redirect
from flask_restplus import Api
from datetime import timedelta

from server.configs import configs
from server.status import HTTPStatus, make_result, APIStatus
from server.logger import log

# flask对象
app = Flask(__name__)
app.config['ERROR_404_HELP'] = False

# flask_restplus对象
api = Api(app, version='4.0.2', title='省省回头车 Feed API 4.0.1',
    description='省省回头车 Feed API 4.0.1', authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Token'
        }
    }, security='apikey', ui=True
)

# session超时时间
app.permanent_session_lifetime = timedelta(days=3)

# 登录验证
@app.before_request
def login_auth():
    # 接口页面
    if request.path == '/' or 'swagger' in request.path:
        pass
    # 静态文件
    elif 'static' in request.path:
        pass
    elif not session.get('login') and request.path != '/login/':
        return redirect('/login/')


# 跨域设置
@app.after_request
def cors(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept, token, appVersion')
    #resp.headers.add(
    #    #'Access-Control-Expose-Headers',
    #)
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,HEAD')
    return resp

# 异常处理
@app.errorhandler(HTTPStatus.NotFound)
def page_not_found(e):
   log.warn('访问了未知路径: [error: %s]' % (e, ), exc_info=True)
   return jsonify(make_result(APIStatus.NotFound)), 404


@app.errorhandler(HTTPStatus.BadRequest)
def bad_request(e):
   log.warn('错误的请求参数: [error: %s]' % (e, ), exc_info=True)
   return jsonify(make_result(APIStatus.InternalServerError)), 400


@app.errorhandler(HTTPStatus.InternalServerError)
def internal_server_error(e):
    log.warn('内部服务发生异常: [error: %s]' % (e,), exc_info=True)
    return jsonify(make_result(APIStatus.InternalServerError)), 500


@api.errorhandler(Exception)
def resource_internal_server_error(e):
   log.warn('服务发生异常: [error: %s]' % (e, ), exc_info=True)
   return jsonify(make_result(APIStatus.InternalServerError)), 500


@api.errorhandler(ValueError)
@api.errorhandler(TypeError)
def value_error(e):
    log.warn('服务发生异常: [error: %s]' % (e, ), exc_info=True)
    return jsonify(make_result(APIStatus.InternalServerError)), 500

# 接口页面展示
if configs.env.deploy != "dev":
    @api.documentation
    def disable_document():
        return api.render_root()