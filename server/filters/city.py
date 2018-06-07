from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus


class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def get_result(goods, vehicle, params):
        # 货源车型
        result = {}
        for i in goods:
            if i['old_vehicle'] or i['new_vehicle']:
                vehicle_name = i['old_vehicle'] if i['old_vehicle'] else i['new_vehicle']
                result.setdefault(vehicle_name, {})
                if i['status'] == 1 or i['status'] == 2:
                    result[vehicle_name]['待接单'] = result[vehicle_name].setdefault('待接单', 0) + 1
                elif i['status'] == 3:
                    result[vehicle_name]['已接单'] = result[vehicle_name].setdefault('已接单', 0) + 1
                elif i['status'] == -1:
                    result[vehicle_name]['已取消'] = result[vehicle_name].setdefault('已取消', 0) + 1
                # 跨城议价
                if params['goods_type'] == 3:
                    if i['call_count'] == 0:
                        result[vehicle_name]['待联系'] = result[vehicle_name].setdefault('待联系', 0) + 1
                    else:
                        result[vehicle_name]['已联系'] =result[vehicle_name] .setdefault('已联系', 0)['已联系'] + 1
        # 接单车型
        for i in vehicle:
            if i['booking_vehicle']:
                result.setdefault(i['booking_vehicle'], {})
                if i['count']:
                    result[i['booking_vehicle']]['已接单车辆'] = result[i['booking_vehicle']].setdefault('已接单车辆', 0) + 1
                else:
                    result[i['booking_vehicle']]['待接单车辆数'] = result[i['booking_vehicle']].setdefault('待接单车辆数', 0) + 1
        # 合并结果
        city_result = {}
        for i in result:
            city_result[i] = [
                {'value': result[i].get('待接单', 0), 'name': '待接单'},
                {'value': result[i].get('已接单', 0), 'name': '已接单'},
                {'value': result[i].get('已取消', 0), 'name': '已取消'},
                {'value': result[i].get('已接单车辆', 0), 'name': '已接单车辆'},
                {'value': result[i].get('待接单车辆数', 0), 'name': '待接单车辆数'},
            ]
            if params['goods_type'] == 3:
                city_result[i].extend([
                    {'value': result[i].get('待联系', 0), 'name': '待联系'},
                    {'value': result[i].get('已联系', 0), 'name': '已联系'}
                ])
        return build_result(APIStatus.Ok, data=city_result), HTTPStatus.Ok


class CityOrderListFilterDecorator(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return build_result(APIStatus.Ok, count=data['order_counts'], data=data['order_detail']), HTTPStatus.Ok
