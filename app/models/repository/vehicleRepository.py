from app import db
from app.models.tables import Vehicle

class VehicleRepository:

    def getByIdUser(self,idUser):
        return db.session.query(Vehicle).filter_by(fk_user = idUser).first()