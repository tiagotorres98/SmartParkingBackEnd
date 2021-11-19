from app import db
from app.models.tables import Vehicle_Model
from sqlalchemy import desc


class VehicleModelRepository() :

    def getAll(self):
        return db.session.query(Vehicle_Model).all()

    def getById(self,id):
        return db.session.query(Vehicle_Model).filter_by(id_modelo_vehicle = id).all()

    def getLastOne(self):
        return db.session.query(Vehicle_Model).order_by(desc('id_modelo_vehicle')).first()
    