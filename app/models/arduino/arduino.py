from app import db
from app.models.tables import Gate_Status
from datetime import datetime

class Gate():

    def open(self):
        gate = Gate_Status(1,1,datetime.today())
        db.session.merge(gate)
        db.session.commit()
    
    def close(self):
        gate = Gate_Status(1,0,datetime.today())
        db.session.merge(gate)
        db.session.commit()