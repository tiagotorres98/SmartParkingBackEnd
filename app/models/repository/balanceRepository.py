from app import db
from app.models.tables import Rent,Service,Rent_Service
from sqlalchemy import cast, Date,func, extract
from datetime import datetime,timedelta

class BalanceRepository:
    
    def balanceFiveDays(self):

        result = [0,0,0,0,0]

        for x in range(5):
            result1 = db.session.query(Rent.id_rent,Rent.hourly_value
            ).filter(Rent.entry_time.cast(Date) == (datetime.today() - timedelta(days=x)).strftime("%Y-%m-%d")
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

    def balanceFiveMonths(self):

        result = [0,0,0,0,0]

        for x in range(5):
            month = int(datetime.today().strftime("%m"))-x

            if month < 0:
                month *= -1

            result1 = db.session.query(Rent.id_rent,Rent.hourly_value
            ).filter(extract('month',Rent.entry_time) == month
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

