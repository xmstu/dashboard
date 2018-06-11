import re


class ExtendHandler(object):
    """扩展类

    """

    @staticmethod
    def handler(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : String
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)

    @staticmethod
    def handler_to_float(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : Float
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else float(obj)


class Check(object):
    @staticmethod
    def is_mobile(mobile) -> bool:
        if mobile and str(mobile).isdigit():
            return bool(re.findall('1[23456789]{1}['
                                   '0-9]{9}', str(mobile)))
        return False
