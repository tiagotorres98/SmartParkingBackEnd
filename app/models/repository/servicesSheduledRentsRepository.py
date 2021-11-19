from app import db
from app.models.tables import ServicesRentalScheduled

class ServicesSheduledRentsRepository():

    def getBySheduledId(self,id):
        return db.session.query(ServicesRentalScheduled
        ).filter_by(fk_sheduled = id
        ).all()
        