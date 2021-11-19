from app import db
from app.models.tables import CreditCard, MonthlyLease

class CreditCardRepository:

    def getCardByIdPerson(self,idPerson):
        return db.session.query(CreditCard).filter_by(fk_person = idPerson).filter_by(ic_active = 1).all()
    
    def getCardById(self,id):
        return db.session.query(CreditCard).filter_by(id_card = id).filter_by(ic_active = 1).first()

    def getCardByNumber(self,num):
        return db.session.query(CreditCard).filter_by(numberCard = num).filter_by(ic_active = 1).all()

    def getDefaultCardByIdPerson(self,idPerson):
        return db.session.query(CreditCard
        ).filter_by(fk_person = idPerson
        ).filter_by(ic_active = 1
        ).filter_by(defaultCard = 1
        ).first()

    def getCCMonthlyLeaseByCardId(self,id):
        return db.session.query(CreditCard,MonthlyLease
        ).filter_by(id_card = id
        ).filter_by(ic_active = 1
        ).join(MonthlyLease,MonthlyLease.fk_creditCard == CreditCard.id_card
        ).filter_by(ic_active = 1
        ).all()

    def returnToJson(self, result):
            card = []
            for x in result:
                y = {
                    "id_card":x.id_card,
                    "ownerName":x.ownerName,
                    "numberCard":x.numberCard,
                    "expirationDate":x.expirationDate.strftime("%m/%Y"),
                    "secCode":x.secCode
                }
                card.append(y)
            return card