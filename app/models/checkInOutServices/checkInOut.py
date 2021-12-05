from app.models.tables import Establishment, EstablishmentDetails, ParkingRating, Rent, Vehicle, Rent_Service
from app.models.repository.vehicleRepository import VehicleRepository
from app.models.repository.sheduledRentsRepository import ScheduledRentsRepository
from app.models.repository.servicesSheduledRentsRepository import ServicesSheduledRentsRepository
from datetime import date, datetime
from app.models.repository.parkingRepository import ParkingRepository
from app.models.repository.rentsRepository import RentsRepository
from app import db

class CheckIn():

    def addRent(self,user):
        try:
            vehicle = VehicleRepository().getByIdUser(user.id)

            scheduled = ScheduledRentsRepository().getByUserId(user.id)

            scheduledServices = ServicesSheduledRentsRepository().getBySheduledId(scheduled[0].id_scheduled)

            esresult = ParkingRepository().getAllParkingsByIdParking(scheduled[0].fk_establishments)
            establishment = ParkingRepository().returnToJson(esresult)[0]

            rents = Rent(vehicle.id_vehicle,user.id,establishment['id'],scheduled[0].start_scheduled,datetime.today(),None,establishment['hour_price'],"")

            db.session.add(rents)
            
            scheduled[0].completed_schedule = datetime.today()
            db.session.merge(scheduled[0])

            rents = RentsRepository().getLastOne()

            for service in scheduledServices:
                p = Rent_Service(rents.id_rent,service.fk_service,None,None)
                db.session.add(p)

            db.session.commit() 
            return {"mensagem":"true"}

        except Exception as e:
            return {"mensagem":str(e)}


class CheckOut():

    def endRent(self,user):
        try:
            rent = RentsRepository().getByIdUser(user.id)
            return self.endRentService(rent)
        except Exception as e:
            return {"mensagem":str(e)}
    
    def endRentService(self,rent):
        try:
            print(rent)
            rent.exit_time = datetime.today()
            db.session.merge(rent)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}

class PublishRating():

    def publish(self,user,rateValue):
        try:
            rent = RentsRepository().getRentNotRated(user.id)
            rate = ParkingRating(user.id,rent.fk_establishments,rateValue)
            db.session.add(rate)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}
