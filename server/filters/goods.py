import time

from server import log
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        goods_detail = data['goods_detail']
        # TODO 过滤参数
        try:
            for detail in goods_detail:

                detail['node_id'] = detail['node_id'] if detail.get('node_id') else "未知网点"

                # 构造货物规格
                goods_standard = []
                if detail['NAME']:
                    goods_standard.append(detail['NAME'])
                if detail['weight']:
                    goods_standard.append(detail['weight'])
                if detail['volume']:
                    goods_standard.append(detail['volume'])
                detail['goods_standard'] = ','.join(goods_standard) if goods_standard else '没有规格'
                detail.pop('NAME')
                detail.pop('weight')
                detail.pop('volume')

                # 构造装货时间
                if detail['loading_time_period_begin'] == 0:
                    loading_time_period = ''
                    if detail['loading_time_period'] == 0:
                        loading_time_period = '00:00:00'
                    if detail['loading_time_period'] == 1:
                        loading_time_period = '07:00:00'
                    if detail['loading_time_period'] == 2:
                        loading_time_period = '12:00:00'
                    if detail['loading_time_period'] == 3:
                        loading_time_period = '19:00:00'
                    detail['loading_time'] = detail['loading_time_date'] + ' ' + loading_time_period
                else:
                    detail['loading_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(detail['loading_time_period_begin']))

                detail.pop('loading_time_period_begin')
                detail.pop('loading_time_date')
                detail.pop('loading_time_period')

            return build_result(APIStatus.Ok, count=data['goods_count'], data=goods_detail), HTTPStatus.Ok
        except Exception as e:
            log.error('Error:{}'.format(e))


