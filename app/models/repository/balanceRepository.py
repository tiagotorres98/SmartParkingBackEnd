from app import db
from app.models.tables import Rent,Service,Rent_Service
from sqlalchemy import cast, Date,func, extract
from datetime import datetime,timedelta
import calendar

class BalanceRepository:
    
    def balanceFiveDays(self,date):

        result = [0,0,0,0,0]

        for x in range(5):
            result1 = db.session.query(Rent.id_rent,Rent.hourly_value
            ).filter(Rent.entry_time.cast(Date) == (date - timedelta(days=x)).strftime("%Y-%m-%d")
            ).all()
            for y in result1:
                    result2 = db.session.query(Rent_Service.fk_service,Service.valor
                    ).filter(Rent_Service.fk_rent == y[0]
                    ).join(Service,Service.id_service == Rent_Service.fk_service
                    ).all()
                    result[x] += y[1]
                    for z in result2:
                        result[x] += z[1]
            
        return result

    def balanceFiveMonths(self,get):
        selectedMonth = get['selectedMonth']
        selectedYear = get['selectedYear']

        result = [0,0,0,0,0,0,0,0,0,0,0,0,0]

        for x in range(12):
            month = int(self.monthByName(selectedMonth))-x
    
            if month < 0:
                month *= -1

            result1 = db.session.query(Rent.id_rent,Rent.hourly_value
            ).filter(extract('month',Rent.entry_time) == month
            ).filter(extract('year',Rent.entry_time) == selectedYear
            ).all()
            for y in result1:
                    result2 = db.session.query(Rent_Service.fk_service,Service.valor
                    ).filter(Rent_Service.fk_rent == y[0]
                    ).join(Service,Service.id_service == Rent_Service.fk_service
                    ).all()
                    result[x] += y[1]
                    for z in result2:
                        result[x] += z[1]
        
        today = datetime.today()
        result1 = db.session.query(Rent.id_rent,Rent.hourly_value
        ).filter(extract('month',Rent.entry_time) == today.strftime('%m')
        ).filter(extract('year',Rent.entry_time) == today.strftime('%Y')
        ).all()
        for y in result1:
                result2 = db.session.query(Rent_Service.fk_service,Service.valor
                ).filter(Rent_Service.fk_rent == y[0]
                ).join(Service,Service.id_service == Rent_Service.fk_service
                ).all()
                print(y)
                result[12] += y[1]
                for z in result2:
                    result[12] += z[1]
            
        return result

    
    def balanceWeek(self,get):
        selectedMonth = get['selectedMonth']
        selectedYear = get['selectedYear']
        selectedWeek = get['selectedWeek']
        month = self.monthByName(selectedMonth)

        result = [0,0,0,0,0,0,0,0]
        for x in range(7):
            
            try:
                date = datetime.strptime(str(selectedYear)+"-"+str(month)+"-"+str((int(selectedWeek[0])-1)*7+x+1),"%Y-%m-%d")
                result1 = db.session.query(Rent.id_rent,Rent.hourly_value
                ).filter(cast(Rent.entry_time,Date) == date
                ).all()
                for y in result1:
                        result2 = db.session.query(Rent_Service.fk_service,Service.valor
                        ).filter(Rent_Service.fk_rent == y[0]
                        ).join(Service,Service.id_service == Rent_Service.fk_service
                        ).all()
                        result[x] += y[1]
                        for z in result2:
                            result[x] += z[1]
            except:
                maxDay = calendar.monthrange(selectedYear, month)[1]
                result = [0,0,0,0,0,0,0,0]
                for x in range(7):  
                    date = datetime.strptime(str(selectedYear)+"-"+str(month)+"-"+str((maxDay-6)+x),"%Y-%m-%d")
                    result1 = db.session.query(Rent.id_rent,Rent.hourly_value
                    ).filter(cast(Rent.entry_time,Date) == date
                    ).all()
                    for y in result1:
                            result2 = db.session.query(Rent_Service.fk_service,Service.valor
                            ).filter(Rent_Service.fk_rent == y[0]
                            ).join(Service,Service.id_service == Rent_Service.fk_service
                            ).all()
                            result[x] += y[1]
                            for z in result2:
                                result[x] += z[1]


                result1 = db.session.query(Rent.id_rent,Rent.hourly_value
                ).filter(cast(Rent.entry_time,Date) == datetime.today().strftime('%Y-%m-%d')
                ).all()
                for y in result1:
                        result2 = db.session.query(Rent_Service.fk_service,Service.valor
                        ).filter(Rent_Service.fk_rent == y[0]
                        ).join(Service,Service.id_service == Rent_Service.fk_service
                        ).all()
                        result[7] += y[1]
                        for z in result2:
                            result[7] += z[1]
                
                
                return result

        return result



    def monthByName(self,name):
        months = ['Janeiro', 'Fevereiro', 'Março', 
                    'Abril', 'Maio', 'Junho' , 'Julho', 
                        'Agosto' ,'Setembro','Outubro', 'Novembro', 'Dezembro']
        
        i = 0
        for m in months:
            i = i+1
            if name == m:
                return i