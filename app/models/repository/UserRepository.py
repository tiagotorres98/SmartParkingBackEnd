from typing import Text
from app import db
from app.models.tables import Telephone, User,Person,Vehicle,Address
from sqlalchemy import desc


class UserRepository:

    def getAll(self):
        return db.session.query(User).all()

    def getById(self,idv):
        return db.session.query(User).filter_by(id = idv).all()

    def getLastOne(self):
        return db.session.query(User).order_by(desc('id')).first()
    
    def getByEmail(self,userEmail):
        return db.session.query(User).filter_by(email = userEmail).first()

    def getAllUserData(self,id):
        return db.session.query(User,Person,Address,Vehicle).join(Person, Person.id_person == User.fk_person
        ).join(Address, Address.fk_person == Person.id_person
        ).join(Vehicle, Vehicle.fk_user == User.id
        ).first()
    
    def getAllUserDataByEmail(self,userEmail):
        return db.session.query(User,Person,Address,Vehicle,Telephone
        ).filter_by(email = userEmail
        ).join(Person, Person.id_person == User.fk_person
        ).join(Address, Address.fk_person == Person.id_person
        ).join(Vehicle, Vehicle.fk_user == User.id
        ).join(Telephone, Telephone.fk_person == Person.id_person
        ).first()
    
    def resultToJson(self,getAllUserData):
        user = {
        "name": str(getAllUserData.Person.name),
        "cpf": str(getAllUserData.Person.cpf),
        "email": str(getAllUserData.User.email),
        "address": str(getAllUserData.Address.address),
        "phone": str(getAllUserData.Telephone.number),
        "birthday": str(getAllUserData.Person.birth_date),
        "sex": str(getAllUserData.Person.sex),
        "password": "",
        "car": {
            "model": str(getAllUserData.Vehicle.model),
            "brand": str(getAllUserData.Vehicle.brand),            
            "color": str(getAllUserData.Vehicle.color),
            "category":"",
            "chassi": str(getAllUserData.Vehicle.chassi),
            "renavam": str(getAllUserData.Vehicle.renavam),
            "plate": str(getAllUserData.Vehicle.plate),
            }
        }   
        return user
