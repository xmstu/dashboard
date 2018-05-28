# -*- coding: utf-8 -*-
import hashlib
import logging
import time

from server import log, read_db, write_db
from server.models.general import UserModel, UserStatsModel
from server.status import message
from server.workflow import utils


class Login(object):

    @staticmethod
    @utils.performance(log=log, level=logging.INFO)
    def add(args):
        """正常登陆"""

        user_id = args['user_id']
        password = args['password']

        user = UserModel.query_one(read_db, id=user_id)

        if not (user and user['password'] == hashlib.md5(password.encode('utf8')).hexdigest()):
            log.info('Login add user_id:%s PasswordError' % user_id)
            raise message.MessageException(message.PasswordError)

        with write_db.begin() as db:

            UserStatsModel.update(db.conn, {'last_login_time': int(time.time())}, user_id=user_id)
            log.debug('Login add user_id:%s _delete_old_token ok' % user_id)
            return args
