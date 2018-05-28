# -*- coding: utf-8 -*-
import hashlib
import logging

from server import log
from server.models.general import UserModel
from server.status import message
from server.workflow import utils


class Login(object):

    @staticmethod
    @utils.performance(log=log, level=logging.INFO)
    def add(user_id, password):
        """正常登陆"""

        user = UserModel.query_one(read_db, id=user_id)

        if not (user and user['password'] == hashlib.md5(password.encode('utf8')).hexdigest()):
            log.info('Login add user_id:%s PasswordError' % user_id)
            raise message.MessageException(message.PasswordError)

        with write_db.begin() as db:
            RefreshTokenModel.update(db.conn, {'is_deleted': 1, 'expired_time': int(time.time())},
                                     user_id=user_id, device_type=device_type, is_deleted=0)
            Login._delete_old_token(db.conn, user_id)
            UserStatsModel.update(db.conn, {'last_login_time': int(time.time())}, user_id=user_id)
            log.debug('Login add user_id:%s _delete_old_token ok' % user_id)
            return Login.common_login(db.conn, user_id)