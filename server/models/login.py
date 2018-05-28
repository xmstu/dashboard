# -*- coding: utf-8 -*-
import hashlib
import logging
import time

from server import log, read_io, write_io
from server.models.general import UserModel, UserStatsModel
from server.status import message
from server.workflow import utils


class Login(object):

    @staticmethod
    @utils.performance(log=log, level=logging.INFO)
    def add(args):
        """正常登陆"""

        user_id = args['user_id']

        with write_io.begin() as db:

            UserStatsModel.update(db.conn, {'last_login_time': int(time.time())}, user_id=user_id)
            log.debug('Login add user_id:%s ok' % user_id)
            return args

    @staticmethod
    def get_user(args):
        mobile = str(args['mobile'])
        password = args['password']
        password = hashlib.md5(password.encode('utf8')).hexdigest()

        result = read_io.query_one("""
                                  SELECT *
                                  FROM shu_users
                                  WHERE `mobile` = :mobile AND `password` = :password AND is_deleted = 0
                                  """, {'mobile': mobile, 'password': password})

        log.info('Result:%s ' % result)
        if result and result.get('id'):
            return result
        else:
            log.info('LoginDecorator common_check %s NotUser' % args['mobile'])
            raise message.MessageException(message.NotUser)
