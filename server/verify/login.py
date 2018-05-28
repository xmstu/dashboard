from server import log
from server.status import UserAPIStatus
from server.status.message import direct_response
from server.utils.extend import Check
from server.workflow.passing import Passing, make_passing


class LoginSetting(object):
    def __init__(self):
        pass

    @staticmethod
    @make_passing
    def post(args):
        if not Check.is_mobile(args.get('mobile')):
            log.info('LoginSetting post mobile error %s' % args.get('mobile'))
            return direct_response({'status': UserAPIStatus.BadRequest, 'msg': '电话号码有错误'})

        return Passing(args=args)
