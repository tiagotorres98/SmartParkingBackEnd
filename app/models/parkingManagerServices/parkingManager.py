from app import db
from app.models.repository.parkingRepository import ParkingRepository
from app.models.repository.servicesRepository import ServicesRepository
from app.models.tables import Establishment, EstablishmentDetails, Service, ParkingService

class ServicesData:

    def addService(self,service,parkingService):
        try:
            db.session.add(service)
            service = ServicesRepository().getLastOne()
            parkingService.fk_services = service.id_service
            db.session.add(parkingService)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}

    def updateService(self,idService,active):
        try:
            parkingService = ServicesRepository().getById(idService)
            parkingService.ic_active = active
            db.session.merge(parkingService)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}

class OpeningHours:

    def updateOpening(self,open,close,day_week_init,day_week_end):
        try:
            esDetail = ParkingRepository().getEstablishmentDetail(1)

            esDetail.time_open = open
            esDetail.time_close = close
            esDetail.day_week_init = day_week_init
            esDetail.day_week_end = day_week_end

            db.session.merge(esDetail)
            db.session.commit()
            return {"mensagem":"true"}
        except Exception as e:
            return {"mensagem":str(e)}
