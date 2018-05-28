#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server.models.login import Login
from server.workflow.passing import Passing, make_passing


class LoginDecorator(object):

    def __init__(self):
        pass

    @staticmethod
    @make_passing
    def common_check(args):
        args = Login.get_user(args)
        return Passing(args=args)
