from server import api

request_jobs_list_param = api.doc(params={
    'job_name': '职位名称',
    'job_type': '职业类别',
    'region': '地区筛选',
    'pub_time': '发布时间筛选',
    'page': '页数',
    'limit': '条数',
}, description='货源统计列表查询参数')
