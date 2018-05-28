#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server import log
from server.meta.decorators import make_decorator
from server.models.login import Login
from server.status import message
from server.workflow.passing import Passing


class LoginDecorator(object):

    def __init__(self):
        pass

    @staticmethod
    @make_decorator
    def common_check(args):
        args = Login.get_user(args)
        return Passing(args=args)

    @staticmethod
    @make_decorator
    def post(args):
        args = Login.add(args)
        return Passing(args=args)
