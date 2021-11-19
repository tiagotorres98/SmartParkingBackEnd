from app import db
from app.models.repository.addressRepository import AddressRepository
from app.models.repository.creditCardRepository import CreditCardRepository
from app.models.repository.monthlyLeaseRepository import MonthlyLeaseRepository
from app.models.repository.PersonRepository import PersonRepository
from app.models.repository.telephoneRepository import TelephoneRepository
from app.models.repository.UserRepository import UserRepository
from app.models.repository.VehicleModelRepository import VehicleModelRepository
from app.models.repository.vehicleRepository import VehicleRepository
from app.models.tables import (Address, CreditCard, MonthlyLease, Person, Telephone, User,
                               Vehicle)
from sqlalchemy import update


class UpdateRegister:
    def update(self,email,addressValue,phone,carModelData,carBrandData,carColorData):
        try:
            user = UserRepository().getByEmail(email);      
            telephone = TelephoneRepository().getByIdPerson(user.fk_person)
            vehicle = VehicleRepository().getByIdUser(user.id)
            address = AddressRepository().getByIdPerson(user.fk_person)

            user.email = email
            address.address = addressValue
            vehicle.model = carModelData
            vehicle.brand = carBrandData
            vehicle.color = carColorData
            telephone.number = phone

            print(address.address)

            db.session.merge(user)
            db.session.merge(telephone)
            db.session.merge(vehicle)
            db.session.merge(address)
            db.session.commit()

            return {"mensagem": "true"}
            
        except Exception as e:
            return {"mensagem": str(e)}
        

class CancelMonthlyLease:

    def cancel(id):
        try:
            monthlyLease = MonthlyLeaseRepository().getMonthlyById(id)
            monthlyLease.ic_active = 0
            db.session.merge(monthlyLease)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}


class CreditCardServices:

    def remove(self,id):
        try:
            card = CreditCardRepository().getCardById(id)
            result = CreditCardRepository().getCCMonthlyLeaseByCardId(id)
            card.ic_active=0
            if len(result) == 0:
                db.session.merge(card)
                db.session.commit()
                return {"mensagem":"true"}
            else:
                return {"mensagem":"Não foi possível remover! O cartão está associado a uma vaga mensal."}
        except Exception as e:
            return {"mensagem":str(e)}
    
    def addCard(self,card):
        try:
            cardRepo = CreditCardRepository().getCardByNumber(card.numberCard)
            if len(cardRepo) == 0:
                card.defaultCard = 0
                db.session.add(card)
                db.session.commit()
                return {"mensagem":"true"}
            else:
                return {"mensagem":"Não foi possível cadastrar! Cartão de Crédito já cadastrado."}
        except Exception as e:
            print(e)
            return {"mensagem":str(e)}
