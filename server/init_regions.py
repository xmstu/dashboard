# coding=utf-8
# author=veficos


from .database import db
from server.utils.init_regions import InitRegionModel

init_regions = InitRegionModel.get_regions(db.read_db)
pass
