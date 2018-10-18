import datetime
import time

vehicle_name = {
    '1': '小面包车',
    '2': '中面包车',
    '3': '小货车',
    '4': '4.2米',
    '5': '6.8米',
    '6': '7.6米',
    '7': '9.6米',
    '8': '13米',
    '9': '17.5米',
}

d_user = {
    1: '新增用户数',
    2: '累计用户数',
    3: '累计认证数',
    4: '登录过人数',
    5: '均有登录人数',
}

d_goods = {
    1: '货源数',
    2: '接单数',
    3: '取消数',
    4: '待接单数',
}

d_vehicle = {
    1: '货源所需车辆',
    2: '累计车辆',
    3: '活跃车辆',
}

d_order = {
    1: '订单数',
    2: '完成订单数',
    3: '进行中',
    4: '已取消',
}

vehicle_name_id = {
    '小面包车': '118',
    '中面包车': '119',
    '小货车': '274',
    '4.2米': '18',
    '5.2米': '36',
    '6.8米': '20',
    '7.6米': '21',
    '9.6米': '23',
    '13米': '31',
    '17.5米': '25',
}

vehicle_id_name = {'118': '小面包车',
                   '119': '中面包车',
                   '274': '小货车',
                   '18': '4.2米',
                   '36': '5.2米',
                   '20': '6.8米',
                   '21': '7.6米',
                   '23': '9.6米',
                   '31': '13米',
                   '25': '17.5米'}

vehicle_name_list = ['小面包车', '中面包车', '小货车', '4.2米', '5.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米']

# 今天日期
today = datetime.date.today()
# 昨天时间
yesterday = today - datetime.timedelta(days=1)
# 明天时间
tomorrow = today + datetime.timedelta(days=1)
acquire = today + datetime.timedelta(days=2)
# 昨天开始时间戳
yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
# 昨天结束时间戳
yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
# 今天开始时间戳
today_start_time = yesterday_end_time + 1
# 今天结束时间戳
today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
# 明天开始时间戳
tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
# 明天结束时间戳
tomorrow_end_time = int(time.mktime(time.strptime(str(acquire), '%Y-%m-%d'))) - 1

# 星期
weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']