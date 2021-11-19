from app import db
from app.models.tables import ScheduledRents
from sqlalchemy import desc

class ScheduledRentsRepository():

    def getByUserId(self,id):
        return db.session.query(ScheduledRents
        ).filter_by(fk_user = id
        ).filter_by(completed_schedule = None
        ).all()
    
    def getLast():
        return db.session.query(ScheduledRents).order_by(desc('id_scheduled')).first()