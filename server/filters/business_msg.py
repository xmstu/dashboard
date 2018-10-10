import re

from server.meta.decorators import make_decorator
from server.status import make_resp, APIStatus, HTTPStatus
from server.utils.calc_dstance import calcDistance


class BusinessMsgList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数
        count = data["count"]
        for detail in data["data"]:
            re_ret = re.findall("经度：(\d{1,3}\.\d{1,6})， 纬度：(\d{1,3}\.\d{1,6})", detail["content"])
            Lat_A, Lng_A = re_ret[0]
            Lat_B, Lng_B = re_ret[1]
            mileage = calcDistance(float(Lat_A), float(Lng_A), float(Lat_B), float(Lng_B))

            ret = re.sub("<br>装货-经纬度.*?镇id：(\d+)", "", detail['content'], re.S)

            ret = re.sub("<br>卸货-经纬度.*?镇id：(\d+)", "", ret, re.S)

            detail['content'] = ret + """<br>里程:%dkm<br>""" % mileage
            detail["msg_type"] = "长期用车"

        return make_resp(APIStatus.Ok, count=count, data=data["data"]), HTTPStatus.Ok
