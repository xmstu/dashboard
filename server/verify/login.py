from server.meta.decorators import make_decorator


class LoginSetting(object):
    def __init__(self):
        pass

    @staticmethod
    @make_decorator
    def post(args):
        if not Check.is_mobile(args.get('mobile')):
            log.info('LoginSetting post mobile error %s' % args.get('mobile'))
            return direct_response({'status': UserAPIStatus.BadRequest, 'msg': '电话号码有错误'})

        if not Limit.ok('loging_%s' % args['mobile']):
            log.info('LoginSetting post Limit error %s' % args.get('mobile'))
            return direct_response({'status': UserAPIStatus.BadRequest, 'msg': '您的请求过于频繁，请稍后重试！'})

        return Passing(args=args)
