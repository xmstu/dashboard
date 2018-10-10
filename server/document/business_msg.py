from flask_restplus import fields

from server import api

request_business_msg_list_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})

request_business_msg_post = api.doc(body=api.model('request_business_msg_post', {
    'follow_name': fields.String(description='跟进人的名字'),
    'follow_result': fields.String(description='谈成或者没谈成的结果'),
}))
