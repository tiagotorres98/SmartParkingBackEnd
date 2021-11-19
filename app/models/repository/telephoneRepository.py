from app import db
from app.models.tables import Telephone

class TelephoneRepository:

    def getByIdPerson(self,idPerson):
        return db.session.query(Telephone).filter_by(fk_person = idPerson).first()