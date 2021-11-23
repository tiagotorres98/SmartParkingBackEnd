from app import db
from app.models.repository.parkingRepository import ParkingRepository
from app.models.tables import Rent, Vacante_Status
from sqlalchemy import desc
from app.models.repository.rentsRepository import RentsRepository

class VacanciesSensorsRepository():

    def getSensorsStatus(self):
        return db.session.query(Vacante_Status).order_by(desc("id")).first()

    def resultToJson(self,result):
        VACANCE_DISPONIBLE = 3

        disponible_vacancies = 0
        busy_vacancies = 0

        busy_vacancies = ord(result.v1) + ord(result.v2) + ord(result.v3)
        disponible_vacancies = VACANCE_DISPONIBLE - busy_vacancies

        json = {
            "vacancy_utilized": VACANCE_DISPONIBLE,
            "disponible_vacancies": disponible_vacancies,
            "busy_vacancies": busy_vacancies
        }
        return json
    
    def resultToJsonVacancies(self,result):
        repo = RentsRepository().getRentNotFinshed()
        detailV1 = None
        detailV2 = None
        detailV3 = None

        if len(repo) == 2:
            repo.append(None)

        if len(repo) == 1:
            repo.append(None)
            repo.append(None)

        if len(repo) == 0:
            repo.append(None)
            repo.append(None)
            repo.append(None)

        if ord(result.v1) == 1:
            for x in repo:
                if x != None:
                    if x.id_rent != None:
                        detailV1 = x.id_rent
                        index = repo.index(x)
                        repo[index] = None
                        break

        if ord(result.v2) == 1:
            for x in repo:
                if x != None:
                    if x != None:
                        detailV2 = x.id_rent
                        index = repo.index(x)
                        repo[index] = None
                        break

        if ord(result.v3) == 1:
            for x in repo:
                if x != None:
                    if x != None:
                        detailV3 = x.id_rent
                        index = repo.index(x)
                        repo[index] = None
                        break
        

        json = {
            "v1": ord(result.v1),
            "v2": ord(result.v2),
            "v3": ord(result.v3),
            "detailV1":detailV1,
            "detailV2":detailV2,
            "detailV3":detailV3
        }
        return json