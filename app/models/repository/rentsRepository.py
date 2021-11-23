from app import db
from app.models.tables import Person, Rent, Vehicle, User
from sqlalchemy import desc
from datetime import datetime

class RentsRepository:

    def getLastOne(self):
        return db.session.query(Rent).order_by(desc("id_rent")).first()

    def getByIdUser(self,idUser):
        return db.session.query(Rent).filter_by(fk_user = idUser).filter_by(exit_time = None).first()

    def getRentNotRated(self,idUser):
        return db.session.query(Rent).filter_by(fk_user = idUser).order_by(desc("exit_time")).first()

    def getRentNotFinshed(self):
        return db.session.query(Rent).filter_by(exit_time = None).all()
        
    def getById(self,id):
        return db.session.query(Rent, Vehicle, User,Person
        ).filter(Rent.id_rent == id
        ).join(User,User.id == Rent.fk_user
        ).join(Vehicle,Vehicle.fk_user == User.id
        ).join(Person,Person.id_person == User.fk_person
        ).first()

    def returnJson(self,result):
        
        json = {
            "name": result.Person.name,
            "user": result.User.email,
            "plate": result.Vehicle.plate,
            "model": result.Vehicle.model,
            "brand": result.Vehicle.brand,
            "date": datetime.strftime(result.Rent.entry_time, "%d/%m/%Y às %H:%M:%S"),
            "value": result.Rent.hourly_value,
            "user_image": "string",
        }
        
        return (json)