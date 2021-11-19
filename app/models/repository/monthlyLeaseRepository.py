from app import db
from app.models.tables import CreditCard, Establishment, EstablishmentDetails, MonthlyLease
from sqlalchemy import desc


class MonthlyLeaseRepository:

        def getByIdUser(self,idUser):
            return db.session.query(MonthlyLease,Establishment,CreditCard,EstablishmentDetails
            ).filter_by(fk_user = idUser
            ).join(Establishment, Establishment.id_establishment == MonthlyLease.fk_establishments
            ).join(CreditCard, CreditCard.id_card == MonthlyLease.fk_creditCard
            ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
            ).all()

        
        def getByIdUserAndIdEstablishment(self,idUser,idEstablishment):
            return db.session.query(MonthlyLease).filter_by(fk_user = idUser
            ).join(Establishment, Establishment.id_establishment == MonthlyLease.fk_establishments
            ).filter_by(id_establishment = idEstablishment
            ).join(CreditCard, CreditCard.id_card == MonthlyLease.fk_creditCard
            ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
            ).order_by(desc('id')).first()

        def getByIdUserAndIdEstablishmentActive(self,idUser,idEstablishment):
            print(db.session.query(MonthlyLease).filter_by(fk_user = idUser
                        ).filter_by(ic_active = 1
                        ).join(Establishment, Establishment.id_establishment == MonthlyLease.fk_establishments
                        ).filter_by(id_establishment = idEstablishment
                        ).join(CreditCard, CreditCard.id_card == MonthlyLease.fk_creditCard
                        ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
                        ))

            return db.session.query(MonthlyLease).filter_by(fk_user = idUser
            ).filter_by(ic_active = 1
            ).join(Establishment, Establishment.id_establishment == MonthlyLease.fk_establishments
            ).filter_by(id_establishment = idEstablishment
            ).join(CreditCard, CreditCard.id_card == MonthlyLease.fk_creditCard
            ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
            ).all()



        def getMonthlyById(self,idM):
            return db.session.query(MonthlyLease).filter_by(id = idM).first()

        def returnToJson(self, result):
            monthlyLease = []
            for x in result:
                qtd = len(x.CreditCard.numberCard)
                number = x.CreditCard.numberCard[qtd - 4:]
                y = {
                    "id": x.MonthlyLease.id,
                    "parkingName" : x.Establishment.name,
                    "expirationDate" : x.MonthlyLease.expirationDate.strftime("%d/%m/%Y"),
                    "lastNumberCreditCard" : number,
                    "value": x.EstablishmentDetails.monthly_lease_value,
                    "ic_active": ord(x.MonthlyLease.ic_active)
                }
                monthlyLease.append(y)
            return monthlyLease