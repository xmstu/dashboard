# -*- coding: utf-8 -*-

from datetime import timedelta

from flask import Flask, render_template
from flask_restplus import Api

from server.configs import configs
from server.logger import log
from server.status import HTTPStatus

# flask对象
app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
app.secret_key = '\x1a\x8dfb#\xb9\xc8\xc3\x05\x86|\xda\x96\xff\xceo3\xf0\xa3\xb8\x8beoW'

<<<<<<< HEAD

=======
>>>>>>> 4935bd3593eb6930cbc83635521b17fa8fdfddb5
# flask_restplus对象
api = Api(app, version='4.0.2', title='省省回头车 BI API 4.0.1',
          description='省省回头车 BI API 4.0.1', authorizations={
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
# @app.before_request
# def login_auth():
#     # 接口页面
#     if request.path == '/' or 'swagger' in request.path:
#         pass
#     # 静态文件
#     elif 'static' in request.path:
#         pass
#     elif not session.get('login') and request.path != '/login/':
#         return redirect('/login/')


# 跨域设置
@app.after_request
def cors(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept, token, appVersion')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,HEAD')
    return resp


# flask异常处理
@app.errorhandler(HTTPStatus.NotFound)
def page_not_found(e):
    log.warn('访问了未知路径: [error: %s]' % (e,), exc_info=True)
    return render_template('/exception/except.html', status_coder=404, title='资源未找到',
                           content='访问了未知路径: [error: %s]' % e)


@app.errorhandler(HTTPStatus.BadRequest)
def bad_request(e):
    log.warn('错误的请求参数: [error: %s]' % (e,), exc_info=True)
    return render_template('/exception/except.html', status_coder=400, title='参数错误', content='错误的请求参数: [error: %s]' % e)


@app.errorhandler(HTTPStatus.InternalServerError)
def internal_server_error(e):
    log.warn('内部服务发生异常: [error: %s]' % (e,), exc_info=True)
    return render_template('/exception/except.html', status_coder=500, title='服务器内部错误',
                           content='内部服务发生异常: [error: %s]' % e)


@api.errorhandler(Exception)
def resource_internal_server_error(e):
    log.warn('服务发生异常: [error: %s]' % (e,), exc_info=True)
    return render_template('/exception/except.html', status_coder=500, title='服务异常', content='服务发生异常: [error: %s]' % e)


@api.errorhandler(ValueError)
@api.errorhandler(TypeError)
def value_error(e):
    log.warn('服务发生异常: [error: %s]' % (e,), exc_info=True)
    return render_template('/exception/except.html', status_coder=500, title='服务异常', content='服务发生异常: [error: %s]' % e)


# 接口页面展示
if configs.env.deploy != "dev":
    @api.documentation
    def disable_document():
        return api.render_root()
