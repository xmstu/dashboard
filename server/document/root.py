from server import api

request_root_management_get = api.doc(params={
    'account': '用户名: data-account属性',
    'region_id': '所属地',
    'page': '页数',
    'limit': '条数',
})

request_root_management_add = api.doc(body=api.model('request_root_management_add', {
    'account': '用户名',
    'password': '密码',
    'region_id': '所属地',
}))

request_root_management_put = api.doc(body=api.model('request_root_management_put', {
    'account': '用户名',
    'password': '密码',
    'region_id': '所属地',
}))