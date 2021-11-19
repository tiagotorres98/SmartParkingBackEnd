from app import db
from app.models.tables import Establishment, ParkingService, Service
from sqlalchemy.orm import aliased

class ServicesRepository:
    def getServicesByEstablishments(self,idEstablishment):

        return db.session.query(Service
        ).join(ParkingService,ParkingService.fk_services == Service.id_service
        ).join(Establishment,Establishment.id_establishment == ParkingService.fk_establishments
        ).filter_by(id_establishment = idEstablishment
        ).all()

    def returnToJson(self, result):
            services = []
            for x in result:
                y = {
                    'service_id':x.id_service,
                    'service_name': x.name,
                    'service_price': x.valor
                }
                services.append(y)
            return services