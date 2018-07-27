from server.utils.usual_vehicle import UsualVehicleModel
from .database import db
from server.utils.init_regions import InitRegionModel

init_regions = InitRegionModel.get_regions(db.read_db)
vehicle_id_list = UsualVehicleModel.get_usual_vehicle_ids(db.read_db)
