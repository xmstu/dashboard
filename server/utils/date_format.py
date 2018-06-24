# -*- coding: utf-8 -*-
import datetime, time, calendar
from server.logger import log

def get_date_aggregate(start_time, end_time, periods, data, date_field='create_time', number_field='count'):
    """日期数据聚合
    start_time: datetime.date类型开始日期
    end_time: datetime.date类型结束日期
    periods: 时间周期,2:日，3:周，4:月
    data: {日期: 数量}字典列表
    date_field: 日期字段名称
    number_field： 数量字段名称
    """
    # 结构化数据
    try:
        date_count = {}
        for count in data:
            if count[date_field]:
                create_time = count[date_field].strftime('%Y-%m-%d') if isinstance(count[date_field], int) else count[
                    'create_time']
                date_count[create_time] = count.get(number_field, 0)
        # 初始、截止时间段
        begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(start_time)), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(end_time)), "%Y-%m-%d")

        xAxis = []
        series = []
        # 日
        if periods == 2:
            date_val = begin_date
            while date_val <= end_date:
                date_str = date_val.strftime("%Y-%m-%d")
                date_count.setdefault(date_str, 0)
                xAxis.append(date_str)
                series.append(date_count[date_str])
                date_val += datetime.timedelta(days=1)
        # 周
        elif periods == 3:
            begin_flag = begin_date
            end_flag = begin_date
            count = 0
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                date_count.setdefault(date_str, sum_count)
                # 本周结束
                if count == 6:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                end_flag += datetime.timedelta(days=1)
                count += 1
        # 月
        elif periods == 4:
            begin_flag = begin_date
            end_flag = begin_date
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                month_lastweek, month_lastday = calendar.monthrange(begin_flag.year, begin_flag.month)
                # 结束日期
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m'))
                    series.append(sum_count)
                else:
                    # 本月结束
                    if end_flag.day == month_lastday and end_flag.month == begin_flag.month:
                        xAxis.append(begin_flag.strftime('%Y/%m'))
                        series.append(sum_count)
                        begin_flag = end_flag + datetime.timedelta(days=1)
                        sum_count = 0
                end_flag += datetime.timedelta(days=1)
        return xAxis, series

    except Exception as e:
        log.error('日期数据聚合异常: [error: %s]' % e)