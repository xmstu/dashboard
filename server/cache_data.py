# coding=utf-8
# author=veficos


from .database import db
from server.utils.init_regions import InitRegionModel
from server.utils.cache_model import FreshOwnerModel, FreshDriverModel

init_regions = InitRegionModel.get_regions(db.read_db)
fresh_owner_ids = FreshOwnerModel.get_fresh_owner_id(db.read_db)
fresh_driver_ids = FreshDriverModel.get_fresh_driver_id(db.read_db)
