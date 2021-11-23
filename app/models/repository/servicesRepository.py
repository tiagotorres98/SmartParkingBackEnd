from app import db
from app.models.tables import Establishment, ParkingService, Rent_Service, Service
from sqlalchemy.orm import aliased
from sqlalchemy import desc

class ServicesRepository:
    def getServicesByEstablishments(self,idEstablishment):

        return db.session.query(Service,ParkingService
        ).join(ParkingService,ParkingService.fk_services == Service.id_service
        ).join(Establishment,Establishment.id_establishment == ParkingService.fk_establishments
        ).filter_by(id_establishment = idEstablishment
        ).all()

    def getLastOne(self):
         return db.session.query(Service).order_by(desc("id_service")).first()

    def getById(self,id):
        return db.session.query(ParkingService).filter(ParkingService.fk_services == id).first()

    def getByRentId(self,id):
        return db.session.query(Rent_Service,Service).filter(Rent_Service.fk_rent == id
        ).join(Service,Service.id_service == Rent_Service.fk_service
        ).all()

    def returnToJson(self, result):
            services = []
            for x in result:
                y = {
                    'service_id':x.Service.id_service,
                    'service_name': x.Service.name,
                    'service_price': x.Service.valor,
                    'active':x.ParkingService.ic_active,
                    'backupActive':x.ParkingService.ic_active,
                }
                services.append(y)
            return services