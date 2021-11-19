from app import db
from app.models.tables import User,Person,Vehicle,Address
from app.models.repository.PersonRepository import PersonRepository
from app.models.repository.VehicleModelRepository import VehicleModelRepository
from app.models.repository.UserRepository import UserRepository


class PersistRegister:
    def persist(self,person,user,car,personAdress,personPhone):
        try:
            db.session.add(person)
            db.session.flush()

            idPerson = PersonRepository().getLastOne().id_person
            user.fk_person = idPerson
            personAdress.fk_person = idPerson
            personPhone.fk_person = idPerson

            db.session.add(personAdress)
            db.session.add(user)
            db.session.add(personPhone)
            db.session.flush()

            idCarModel = VehicleModelRepository().getLastOne().id_modelo_vehicle
            idUser = UserRepository().getLastOne().id

            car.fk_user = idUser
            car.fk_model = idCarModel

            db.session.add(car)
            db.session.commit()

            return ""
            
        except Exception as e:
            return str(e)
        
