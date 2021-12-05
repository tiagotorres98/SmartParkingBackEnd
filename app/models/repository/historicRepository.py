from app import db
from app.models.repository.servicesRepository import ServicesRepository
from app.models.tables import Establishment, Rent, Service,User,Person, Vehicle, Vehicle_Brand, Vehicle_Model
from datetime import datetime

class HistoricRepository:

        def getHistoricByIdUser(self,id):
            return db.session.query(Rent,Establishment
            ).filter_by(fk_user = id
            ).join(Establishment,Establishment.id_establishment == Rent.fk_establishments
            ).all()
        
        def getHistoricByIdEstablishment(self,id):
            return db.session.query(Rent,Establishment,User,Person,Vehicle
            ).filter(Rent.fk_establishments == id
            ).filter(Rent.exit_time != None
            ).join(Establishment,Establishment.id_establishment == Rent.fk_establishments
            ).join(User,User.id == Rent.fk_user
            ).join(Person,Person.id_person == User.fk_person
            ).join(Vehicle,Vehicle.fk_user == User.id
            ).all()
        
        def returnToJsonVacancyDetails(self,result):
            historic = []
            print(result)
            for x in result:
                services = []
                servicesValue = 0
                repo = ServicesRepository().getByRentId(x.Rent.id_rent)
                for r in repo:
                    services.append({"name":r.Service.name,"value":r.Service.valor})
                    servicesValue += r.Service.valor

                y = {
                    'usuario': x.Person.name, 
                    'data': datetime.strftime( x.Rent.entry_time, "%d/%m/%Y"),  
                    'placa':  x.Vehicle.plate, 
                    'periodo':  str(x.Rent.exit_time - x.Rent.entry_time), 
                    'valorTotal':  "R$ " + str(x.Rent.hourly_value + servicesValue),
                    'valor':"R$ " + str(x.Rent.hourly_value),
                    'imagem': '../../assets/images/perfil.jpeg',
                    "id_rent":x.Rent.id_rent,
                    "brand":x.Vehicle.brand,
                    "model":x.Vehicle.model,
                    'entry_time':str(x.Rent.entry_time.strftime("%H:%M:%S")),
                    'exit_time':str(x.Rent.exit_time.strftime("%H:%M:%S")),
                    'services':services
                }
                historic.append(y)
            print(historic)
            return historic

        def returnToJsonVacancyDetails2(self,result):
            #Rent,Establishment,User,Person,Vehicle
            historic = []
            for x in result:
                y = {
                    "id_rent":x.Rent.id_rent,
                    "plate":x.Vehicle.plate,
                    "brand":x.Vehicle.brand,
                    "model":x.Vehicle.model,
                    'entry_time':str(x.Rent.entry_time.strftime("%H:%M:%S")),
                    'exit_time':str(x.Rent.exit_time.strftime("%H:%M:%S"))
                }
                historic.append(y)
            print(historic)
            return historic

        def returnToJson(self, result):
            historic = []
            
            for x in result:
                servicesValue = 0
                t = x.Rent.exit_time
                timeout = ""
                if t == None:
                    timeout = "Em uso"
                else:
                    timeout =  x.Rent.exit_time.strftime("%H:%M:%S")
                
                repo = ServicesRepository().getByRentId(x.Rent.id_rent)
                for r in repo:
                    servicesValue += r.Service.valor

                y = {
                    'parking_name': x.Establishment.name, 
                    'date': x.Rent.scheduling_date.strftime("%d/%m/%Y"), 
                    'price': x.Rent.hourly_value + servicesValue, 
                    'timeIn' : x.Rent.entry_time.strftime("%H:%M:%S"), 
                    'timeOut' : timeout
                }
                historic.append(y)
            return historic