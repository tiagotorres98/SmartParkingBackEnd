from app import db
from app.models.repository.ratingRepository import RatingRepository
from app.models.tables import Establishment, EstablishmentDetails, MonthlyLease, ParkingRating, ParkingService, Rent, ScheduledRents, Service
from sqlalchemy.orm import aliased
import math
from sqlalchemy.sql import func

class ParkingRepository:

    def getEstablishmentDetail(self,id):
        return db.session.query(EstablishmentDetails
        ).filter(EstablishmentDetails.fk_establishments == id
        ).first()

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
    
    def returnToJsonParkingManager(self,result):
        json = {
            "open": str(result[0].EstablishmentDetails.time_open)[0:5],
            "close": str(result[0].EstablishmentDetails.time_close)[0:5],
            "day_week_init": result[0].EstablishmentDetails.day_week_init,
            "day_week_end": result[0].EstablishmentDetails.day_week_end
        }
        return json

    def returnToJsonParkingManagerRegister(self,result):
        #Establishment,EstablishmentDetails
        json = {
            "fantasy_name":result[0].Establishment.name,
            "vacancies_number":result[0].EstablishmentDetails.num_vacancies,
            "company_email":result[0].Establishment.email,
            "hour_price":result[0].EstablishmentDetails.hour_value,
            "company_address":result[0].Establishment.address,
            "daily_price":result[0].EstablishmentDetails.hour_value,
            "cnpj":result[0].Establishment.cnpj,
            "monthly_vacancies":result[0].EstablishmentDetails.num_monthly_vacancies,
            "social_reason":result[0].Establishment.social_reason,
            "monthly_price":result[0].EstablishmentDetails.monthly_lease_value,
            "apresentation_image":"",
            "password":"",
        }
        return json

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
