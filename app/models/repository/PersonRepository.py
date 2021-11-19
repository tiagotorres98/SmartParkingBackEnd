from app import db
from app.models.tables import Person
from sqlalchemy import desc


class PersonRepository:

    def getByCPF(self,cpfV):
        query = db.session.query(Person).filter_by(cpf = cpfV)
        return query.first()

    def getAll(self):
        return db.session.query(Person).all()

    def getById(self,id):
        return db.session.query(Person).filter_by(id_person = id).all()

    def getLastOne(self):
        return db.session.query(Person).order_by(desc('id_person')).first()
    