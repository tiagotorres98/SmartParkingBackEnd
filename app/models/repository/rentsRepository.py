from app import db
from app.models.tables import Rent
from sqlalchemy import desc

class RentsRepository:

    def getLastOne(self):
        return db.session.query(Rent).order_by(desc("id_rent")).first()

    def getByIdUser(self,idUser):
        return db.session.query(Rent).filter_by(fk_user = idUser).filter_by(exit_time = None).first()

    def getRentNotRated(self,idUser):
        return db.session.query(Rent).filter_by(fk_user = idUser).order_by(desc("exit_time")).first()