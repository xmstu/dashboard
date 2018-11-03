from server import api

request_jobs_list_param = api.doc(params={
    'job_name': '职位名称',
    'region': '地区筛选',
    'time_scale': '发布时间筛选,0:不限,1:一天以内,2:三天以内,3:七天以内,4:十五天以内,5:一个月以内',
    'page': '页数',
}, description='职位统计列表查询参数')

request_jobs_pie_params = api.doc(params={
    'search_name': '职位名称',
}, description='职位地区分布查询参数')

request_jobs_salary_pie_params = api.doc(params={
    'search_name': '职位名称',
    'region': '地区筛选',
}, description='职位薪水分布查询参数')
