from app import db
from app.models.repository.ratingRepository import RatingRepository
from app.models.tables import Establishment, EstablishmentDetails, MonthlyLease, ParkingRating, ParkingService, Rent, ScheduledRents, Service
from sqlalchemy.orm import aliased
import math
from sqlalchemy.sql import func

class ParkingRepository:

    def getAllParkings(self):
        return db.session.query(Establishment,EstablishmentDetails
        ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
        ).all()
    
    def getAllParkingsByIdParking(self,id):
        return db.session.query(Establishment,EstablishmentDetails
        ).filter_by(id_establishment = id).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
        ).all()

    def getByFilter(self,user_avaliation,minValue,maxValue,parkingNameSearch):
        finalParkings = []
        parkings = db.session.query(Establishment,EstablishmentDetails
        ).join(EstablishmentDetails, EstablishmentDetails.fk_establishments == Establishment.id_establishment
        ).filter(Establishment.name.like("%"+parkingNameSearch+"%")
        ).filter(EstablishmentDetails.hour_value.between(minValue,maxValue)
        ).all()

        for x in parkings:
            if  RatingRepository().getAVGByIdEstablishment(x.Establishment.id_establishment)[1] == user_avaliation or user_avaliation == 0:
                finalParkings.append(x)
                
        return finalParkings



    def getNumberAvailableVacancies(self,idEst):
        rentsNumber = db.session.query(func.count(Rent.id_rent)).filter_by(fk_establishments = idEst).filter_by(exit_time = None).first()
        monthlyLeaseNumber = db.session.query(func.count(MonthlyLease.id)).filter_by(fk_establishments = idEst).filter_by(ic_active = 1).first()
        shceduled = db.session.query(func.count(ScheduledRents.id_scheduled)).filter_by(fk_establishments = idEst).filter_by(completed_schedule = None).first()
        return rentsNumber[0] + monthlyLeaseNumber[0] + shceduled[0]

    def returnToJson(self, result):
            userAvaliation = 0
            parkings = []
            for x in result:
                rating = RatingRepository().getAVGByIdEstablishment(x.Establishment.id_establishment)
                numVacancies = self.getNumberAvailableVacancies(x.Establishment.id_establishment)
                if rating != [] and rating != None:
                    userAvaliation = rating[1]

                if numVacancies == x.EstablishmentDetails.num_vacancies:
                    break
                
                print(numVacancies)
                y = {
                        'id': x.Establishment.id_establishment,
                        'name': x.Establishment.name,
                        'hour_price': x.EstablishmentDetails.hour_value,
                        'monthly_price': x.EstablishmentDetails.monthly_lease_value,
                        'user_avaliation': math.ceil(userAvaliation),
                        'address': x.Establishment.address,
                        'reference_point': x.Establishment.reference_point,
                        'image_url': '../../assets/images/teste.png',
                        'monthly': x.EstablishmentDetails.ic_monthly_lease,
                        'available_vacancies': x.EstablishmentDetails.num_vacancies - numVacancies,
                        'services_available': ""
                    }
                parkings.append(y)
            return parkings