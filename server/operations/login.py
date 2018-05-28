#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server import log
from server.meta.decorators import make_decorator
from server.models.login import Login
from server.models.token import get_user_id_by_mobile, check_user_disabled
from server.status import message
from server.workflow.passing import Passing


class LoginDecorator(object):

    def __init__(self):
        pass

    @staticmethod
    @make_decorator
    def common_check(args):
        user_id = get_user_id_by_mobile(args['mobile'])

        if not user_id:
            log.info('LoginDecorator common_check %s NotUser' % args['mobile'])
            raise message.MessageException(message.NotUser)

        if check_user_disabled(user_id):
            log.info('LoginDecorator common_check %s UserFreeze' % user_id)
            raise message.MessageException(message.UserFreeze)
        else:
            args['user_id'] = user_id

        return Passing(args=args)

    @staticmethod
    @make_decorator
    def post(args):
        result = Login.add(args['user_id'], args['password'])
        return Passing(args=result)
