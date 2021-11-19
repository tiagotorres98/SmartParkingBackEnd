from app import db
from app.models.repository.creditCardRepository import CreditCardRepository
from app.models.repository.monthlyLeaseRepository import MonthlyLeaseRepository
from app.models.repository.servicesRepository import ServicesRepository
from app.models.repository.sheduledRentsRepository import ScheduledRentsRepository
from app.models.tables import MonthlyLease, ScheduledRents, ServicesRentalScheduled

class AddSheduledLease():
    def add(self, sheduledRent,servicesSelected):
        print(servicesSelected)
        try:
            result = ScheduledRentsRepository().getByUserId(sheduledRent.fk_user)
            services = ServicesRepository().getServicesByEstablishments(sheduledRent.fk_establishments)
            if len(result) > 0:
                return {"mensagem":"Você já possui uma vaga pré agendada. Realize sua entrada ou aguarde os 15 minutos para cancelar o agendamento."}
            else:    
                db.session.add(sheduledRent)
                result = ScheduledRentsRepository.getLast()

                for service in servicesSelected:
                    s = ServicesRentalScheduled(result.id_scheduled,service)
                    db.session.add(s)

                db.session.commit()
                return {"mensagem":"true"}

        except Exception as e:
            return {"mensagem":str(e)}

class AddMonthlyLease():
    def add(self,monthlyLease,defaultCardValue):
        creditCard = CreditCardRepository().getCardById(monthlyLease.fk_creditCard)
        defaultCardNow = CreditCardRepository().getCardById(monthlyLease.fk_creditCard)
        monthlyLeaseRepo = MonthlyLeaseRepository().getByIdUserAndIdEstablishmentActive(monthlyLease.fk_user,monthlyLease.fk_establishments)
        try:
            print(len(monthlyLeaseRepo))
            if int(len(monthlyLeaseRepo)) == int(0):
                monthlyLease.ic_active = 1
                db.session.add(monthlyLease)
                if defaultCardValue == 1:
                    creditCard.defaultCard = 1
                    defaultCardNow.defaultCard = 0
                    db.session.merge(defaultCardNow)
                    db.session.merge(creditCard)
                db.session.commit()
                return{"mensagem":"true"}
            else:
                 return {"mensagem":"Não foi possível locar vaga. Você já possui uma vaga mensal neste estabelecimento."}
        except Exception as e:
            return {"mensagem":str(e)}