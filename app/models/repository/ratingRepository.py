from app import db
from sqlalchemy.sql import func

from app.models.tables import ParkingRating

class RatingRepository:

    def getAVGByIdEstablishment(self,id_establishment):
        return db.session.query(ParkingRating.fk_establishments,func.avg(ParkingRating.rating).label('average')
        ).filter_by(fk_establishments = id_establishment
        ).group_by(ParkingRating.fk_establishments).first()
    