from flask_restplus import Resource
import server.document.job_list as doc
from server import api
from server.operations.boss_crawler import boss_spider
from server.status import make_resp, APIStatus
from server.utils.request import get_all_arg
from server.verify.job_list import check_jobs_list


class JobList(Resource):

    @staticmethod
    @doc.request_jobs_list_param
    def get():
        params = get_all_arg()
        params = check_jobs_list(params)
        result = boss_spider(params)
        return make_resp(status=APIStatus.Ok, data=result)


ns = api.namespace('jobs', description='职位统计')
ns.add_resource(JobList, '/jobs_list/')
