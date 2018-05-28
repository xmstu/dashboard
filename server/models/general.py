# coding=utf-8
# author=qiao
from server import log
from server.models import WriteORMModel, ReadORMModel, BaseModel


class CaptchaLogModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shn_captcha_logs'
    description = "shn_captcha_logs"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_users'
    description = "shu_users"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserWalletsModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_wallets'
    description = "shu_wallets"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserImModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_im_accounts'
    description = "shu_im_accounts"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class TokenModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_tokens'
    description = "shu_tokens"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class RefreshTokenModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_refreshtokens'
    description = "shu_refreshtokens"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserRecommendModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_recommended_users'
    description = "shu_recommended_users"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserProfileModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_user_profiles'
    description = "shu_user_profiles"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserStatsModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_user_stats'
    description = "shu_user_stats"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class MiniProgramUserModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shw_miniprogram_accounts'
    description = "shw_miniprogram_accounts"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e


class UserBlockLogModel(BaseModel, ReadORMModel, WriteORMModel):
    table = 'shu_user_ban_logs'
    description = "shu_user_ban_logs"

    def handler(self, e, description, doc, *args, **kwargs):
        log.error("%s %s 失败 arg=%s kwarg=%s" % (description, doc, args, kwargs), exc_info=True)
        raise e
