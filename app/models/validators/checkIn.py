from app.models.repository.rentsRepository import RentsRepository
from app.models.repository.sheduledRentsRepository import ScheduledRentsRepository
from app.models.tables import Rent, ScheduledRents, Vehicle
from app.models.repository.vehicleRepository import VehicleRepository
from datetime import date, datetime

class CheckInByCode():
    def check(self,userCode,idUser):
        
        sheduled = ScheduledRentsRepository().getByUserId(idUser)

        if self.checkHasSchedule(sheduled) == False:
            return {"mensagem":"Você não tem uma locação ativa, verifique seus dados! \
            Caso de mais 2 tentativas de acesso seu usuário será bloqueado por 15 dias"}

        elif self.checkTimeScheduled(sheduled) == False:
            return {"mensagem":"O Tempo da sua reserva expirou. Para acessar o estacionamento será necessário agendar novamente."}

        elif self.checkCode(userCode) == False:
            return {"mensagem":"O código digitado está incorreto. Caso necessário, solicite ajuda a um funcionário do estabelecimento."}
        
        else:
            return {"mensagem":"true"}

    def checkTimeScheduled(self,sheduled):
        print(datetime.today())
        print(sheduled[0].end_scheduled)
        if  datetime.today() > sheduled[0].end_scheduled:
            return False
    
    def checkHasSchedule(self,sheduled):
        if len(sheduled) == 0 and sheduled == []:
            return False
    
    def checkCode(self,codes):
        CODE = 12345678
        if int(codes) != int(CODE):
            return False


class CheckOutByCode():
    def check(self,userCode,idUser):
        
        rents = RentsRepository().getByIdUser(idUser)

        if self.checkHasRents(rents) == False:
            return {"mensagem":"Você não tem uma locação ativa, verifique seus dados! \
            Caso de mais 2 tentativas de acesso seu usuário será bloqueado por 15 dias"}

        elif self.checkCode(userCode) == False:
            return {"mensagem":"O código digitado está incorreto. Caso necessário, solicite ajuda a um funcionário do estabelecimento."}
        
        else:
            return {"mensagem":"true"}

    def checkHasRents(self,rents):
        if rents == None and rents == []:
            return False
    
    def checkCode(self,codes):
        CODE = 12345678
        if int(codes) != int(CODE):
            return False

            

