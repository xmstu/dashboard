from flask_restplus import Resource
import server.document.job_list as doc
from server import api
from server.utils.request import get_all_arg


class JobList(Resource):

    @staticmethod
    @doc.request_jobs_list_param
    def get():
        params = get_all_arg()


ns = api.namespace('jobs', description='职位统计')
ns.add_resource(JobList, '/jobs_list/')
