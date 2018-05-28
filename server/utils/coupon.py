# coding=utf-8
# author=qiao

from server import log, configs, msgqueue


def generate_coupon(user_id, coupon_type):
    try:
        msg = {'user_id': user_id, 'event_key': coupon_type}
        msgqueue.open_event_producer.push(configs.remote.admin_service.msgqueue.coupon.active_coupon.topic,
                                          configs.remote.admin_service.msgqueue.coupon.active_coupon.partition,
                                          msg)
        return True
    except Exception as e:
        log.warn('优惠卷服务异常: [user_id: %s][coupon_type: %s][error: %s]' % (user_id, coupon_type, e), exc_info=True)
    return False
