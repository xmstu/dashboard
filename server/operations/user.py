# -*- coding: utf-8 -*-
from server.meta.decorators import make_decorator


class UserListDecorator(object):

    @staticmethod
    @make_decorator
    def get():
        pass