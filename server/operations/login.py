#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server.meta.decorators import make_decorator


class LoginDecorator(object):

    def __init__(self):
        pass

    @make_decorator
    def common_check(self):
        pass

    @make_decorator
    def post(self):
        pass
