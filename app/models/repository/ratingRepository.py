from app import db
from sqlalchemy.sql import func

from app.models.tables import Establishment, ParkingRating

class RatingRepository:

    def getAVGByIdEstablishment(self,id_establishment):
        return db.session.query(ParkingRating.fk_establishments,func.avg(ParkingRating.rating).label('average')
        ).filter_by(fk_establishments = id_establishment
        ).group_by(ParkingRating.fk_establishments).first()

    def getByIdEstablishment(self,id_establishment):
        return db.session.query(ParkingRating
        ).filter_by(fk_establishments = id_establishment
        ).join(Establishment,Establishment.id_establishment == ParkingRating.fk_establishments
        ).all()
    
    def returnToJsonMonitor(self,result):
        very_satisfied = 0
        satisfied = 0
        medium = 0
        bad = 0
        very_bad = 0
        total = 0

        for x in result:
            total += 1
            if x.rating == 5:
                very_satisfied += 1

            elif x.rating == 4:
                satisfied += 1

            elif x.rating == 3:
                medium += 1

            elif x.rating == 2:
                bad += 1

            elif x.rating == 1:
                very_bad += 1                                            

        json = {
            "very_satisfied": very_satisfied,
            "satisfied": satisfied,
            "medium": medium,
            "bad": bad,
            "very_bad": very_bad,
            "total":total
        }
        return json