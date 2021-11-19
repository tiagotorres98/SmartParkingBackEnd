from app import db
from app.models.tables import Address

class AddressRepository:

    def getByIdPerson(self,idPerson):
        return db.session.query(Address).filter_by(fk_person = idPerson).first()