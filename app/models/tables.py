from os import set_inheritable
from app import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fk_person = db.Column(db.Integer, db.ForeignKey("person.id_person"))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    person = db.relationship("Person", foreign_keys=fk_person)

    def __init__(self, fk_person, email, password, type, status):
        self.fk_person = fk_person
        self.email = email
        self.password = password
        self.type = type
        self.status = status

    def get_id(self):
        return self.email

class Person(db.Model):
    __tablename__ = "person"
    
    id_person = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(30), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)

    def __init__(self, name, birth_date, sex, cpf):
        self.name = name
        self.birth_date = birth_date
        self.sex = sex
        self.cpf = cpf

class Telephone(db.Model):
    __tablename__ = "telephones"

    id_telephone = db.Column(db.Integer, primary_key=True)
    fk_person = db.Column(db.Integer, db.ForeignKey("person.id_person"))
    type = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(30), unique=True, nullable=False)

    person = db.relationship("Person", foreign_keys=fk_person)

    def __init__(self, fk_person, type, number):
        self.fk_person = fk_person
        self.type = type
        self.number = number

class Address(db.Model):
    __tablename__ = "addresses"

    id_address = db.Column(db.Integer, primary_key=True)
    fk_person = db.Column(db.Integer, db.ForeignKey("person.id_person"))
    address = db.Column(db.String(200), nullable=False)

    person = db.relationship("Person", foreign_keys=fk_person)

    def __init__(self, fk_person, address):
        self.fk_person = fk_person
        self.address = address
'''
class City(db.Model):
    __tablename__ = "cities"

    id_city = db.Column(db.Integer, primary_key=True)
    fk_state = db.Column(db.Integer, db.ForeignKey("states.id_state"))
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=True)

    state = db.relationship("State", foreign_keys=fk_state)

    def __init__(self, fk_state, name, desc):
        self.fk_state = fk_state
        self.name = name
        self.desc = desc
    
    def __repr__(self):
        return "<City %r" % self.name

class State(db.Model):
    __tablename__ = "states"

    id_state = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    initials = db.Column(db.String(10), nullable=False)  #sigla
    desc = db.Column(db.String(100), nullable=False)  #descrição

    def __init__(self, name, initials, desc):
        self.name = name
        self.initials = initials
        self.desc = desc

    def __repr__(self):
        return "<State %r" % self.name

##/// finalização parte de usuário e person


class Owner(db.Model):
    __tablename__ = "owners"

    id_owner = db.Column(db.Integer, primary_key=True)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    fk_establishment = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))

    user = db.relationship("User", foreign_keys=fk_user)
    establishment = db.relationship("Establishment", foreign_keys=fk_establishment)

    def __init__(self, fk_user, fk_establishment):
        self.fk_user = fk_user
        self.fk_establishment = fk_establishment

    def __repr__(self):
        return "<State %r" % self.id_owner
'''
class MonthlyLease(db.Model):
    __tablename__ = "monthly_lease"
    id = db.Column(db.Integer, primary_key=True)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id")) 
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))
    fk_creditCard = db.Column(db.Integer, db.ForeignKey("creditCard.id_card"))
    hiringDate = db.Column(db.Date, nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)
    ic_active = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", foreign_keys=fk_user)
    establishments = db.relationship("Establishment", foreign_keys=fk_establishments)
    creditCard = db.relationship("CreditCard", foreign_keys=fk_creditCard)
    
    def __init__(self, fk_user, fk_establishments, fk_creditCard,hiringDate,expirationDate):
        self.fk_user = fk_user
        self.fk_establishments = fk_establishments
        self.fk_creditCard = fk_creditCard
        self.expirationDate = expirationDate
        self.hiringDate = hiringDate


class Establishment(db.Model):
    __tablename__ = "establishments"
    
    id_establishment = db.Column(db.Integer, primary_key=True)
    social_reason = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    reference_point = db.Column(db.String(255), nullable=False)
    social_reason = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __init__(self, social_reason, name, cnpj, address, reference_point,email):
        self.social_reason = social_reason
        self.name = name
        self.cnpj = cnpj
        self.address = address
        self.reference_point = reference_point
        self.email = email

class EstablishmentDetails(db.Model):
    __tablename__ = "establishments_details"
    
    id = db.Column(db.Integer, primary_key=True)
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))
    num_vacancies = db.Column(db.Integer)
    hour_value = db.Column(db.Float)
    daily_value = db.Column(db.Float)
    ic_monthly_lease = db.Column(db.Boolean, nullable=False)
    num_monthly_vacancies = db.Column(db.Integer)
    monthly_lease_value = db.Column(db.Float)
    time_open = db.Column(db.Time)
    time_close = db.Column(db.Time)
    day_week_init = db.Column(db.String(20))
    day_week_end = db.Column(db.String(20))
    
    parking_spaces = db.relationship("Establishment", foreign_keys=fk_establishments)    

    def __init__(self, fk_establishments, num_vacancies, hour_value,daily_value,ic_monthly_lease,num_monthly_vacancies,monthly_lease_value):
        self.fk_establishments = fk_establishments
        self.num_vacancies = num_vacancies
        self.hour_value = hour_value
        self.daily_value = daily_value
        self.ic_monthly_lease = ic_monthly_lease
        self.ic_monthly_lease = ic_monthly_lease
        self.num_monthly_vacancies = num_monthly_vacancies
        self.monthly_lease_value = monthly_lease_value

class Parking_Space(db.Model):
    __tablename__ = "parking_spaces"

    id_parking_space = db.Column(db.Integer, primary_key=True)
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))
    name = db.Column(db.String(80), nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    localization = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    desc = db.Column(db.String(500), nullable=True)

    parking_spaces = db.relationship("Establishment", foreign_keys=fk_establishments)    

    def __init__(self, name, floor, localization, status, desc):
        self.name = name
        self.floor = floor
        self.localization = localization
        self.status = status
        self.desc = desc

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id_vehicle = db.Column(db.Integer, primary_key=True)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id")) 
    model = db.Column(db.String(50), nullable=False) 
    brand = db.Column(db.String(50), nullable=False) 
    plate = db.Column(db.String(40), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    renavam = db.Column(db.String(60), unique=True, nullable=False)
    chassi = db.Column(db.String(60), unique=True, nullable=False)

    user = db.relationship("User", foreign_keys=fk_user)

    def __init__(self,fk_user, model, plate, color, renavam, chassi,brand):
        self.fk_user = fk_user
        self.model = model
        self.plate = plate
        self.color = color
        self.renavam = renavam
        self.chassi = chassi
        self.brand = brand



class Vehicle_Model(db.Model):
    __tablename__ = "vehicle_models"

    id_modelo_vehicle = db.Column(db.Integer, primary_key=True)
    fk_vehicle_brand = db.Column(db.Integer, db.ForeignKey("vehicles_brands.id_vehicle_brand")) 
    fk_vehicle_category = db.Column(db.Integer, db.ForeignKey("vehicle_category.id_vehicle_category")) 
    name = db.Column(db.String(40), nullable=True)
    desc = db.Column(db.String(100), nullable=True)

    vehicle_brand = db.relationship("Vehicle_Brand", foreign_keys=fk_vehicle_brand)
    vehicle_category = db.relationship("Vehicle_Category", foreign_keys=fk_vehicle_category)

    def __init__(self, fk_vehicle_brand, fk_vehicle_category, name, desc):
        self.fk_vehicle_brand = fk_vehicle_brand
        self.fk_vehicle_category = fk_vehicle_category
        self.name = name
        self.desc = desc



class Vehicle_Category(db.Model):
    __tablename__ = "vehicle_category"

    id_vehicle_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    desc = db.Column(db.String(40), nullable=False)

    def __init__(self, id_vehicle_category, name, desc):
        self.id_vehicle_category = id_vehicle_category
        self.name = name
        self.desc = desc
    
    def __repr__(self):
        return "<Vehicle_Category %r" % self.name

class Vehicle_Brand(db.Model):
    __tablename__ = "vehicles_brands"

    id_vehicle_brand = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    desc = db.Column(db.String(40), nullable=False)

    def __init__(self, id_vehicle_brand, name, desc):
        self.id_vehicle_brand = id_vehicle_brand
        self.name = name
        self.desc = desc
    
    def __repr__(self):
        return "<Vehicle_Brand %r" % self.name    

class CreditCard(db.Model):
    __tablename__ = "creditCard"

    id_card = db.Column(db.Integer, primary_key=True)
    fk_person = db.Column(db.Integer, db.ForeignKey("person.id_person"))
    ownerName = db.Column(db.String(80), nullable=False)
    numberCard = db.Column(db.String(30), nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)
    secCode = db.Column(db.Integer, nullable=False)
    ic_active = db.Column(db.Integer, nullable=False)
    defaultCard = db.Column(db.Boolean, nullable=False)

    person = db.relationship("Person", foreign_keys=fk_person)

    def __init__(self, fk_person, ownerName, numberCard, expirationDate, secCode,ic_active):
        self.fk_person = fk_person
        self.ownerName = ownerName
        self.numberCard = numberCard
        self.expirationDate = expirationDate
        self.secCode = secCode
        self.ic_active = ic_active
        

####  Tabelas específicas de locação

class Rent(db.Model):
    __tablename__ = "rents"

    id_rent = db.Column(db.Integer, primary_key=True)
    fk_vehicle = db.Column(db.Integer, db.ForeignKey("vehicles.id_vehicle")) 
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id")) 
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))
    scheduling_date = db.Column(db.DateTime, nullable=False)
    entry_time = db.Column(db.DateTime, nullable=True)
    exit_time = db.Column(db.DateTime, nullable=True)
    hourly_value = db.Column(db.Float, nullable=False)
    desc = db.Column(db.String(400), nullable=True)

    establishment = db.relationship("Establishment", foreign_keys=fk_establishments)
    vehicle = db.relationship("Vehicle", foreign_keys=fk_vehicle)
    user = db.relationship("User", foreign_keys=fk_user)
    
    def __init__(self, fk_vehicle, fk_user, fk_establishments,scheduling_date, entry_time, exit_time, hourly_value, desc):
        self.fk_vehicle = fk_vehicle
        self.fk_user = fk_user
        self.fk_establishments = fk_establishments
        self.scheduling_date = scheduling_date
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.hourly_value = hourly_value
        self.desc = desc

class ParkingRating(db.Model):
    __tablename__ = "parking_rating"

    id = db.Column(db.Integer, primary_key=True)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id")) 
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment")) 
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", foreign_keys=fk_user)
    establishment = db.relationship("Establishment", foreign_keys=fk_establishments)

    def __init__(self, fk_user, fk_establishments, rating):
        self.fk_user = fk_user
        self.fk_establishments = fk_establishments
        self.rating = rating

class Service(db.Model):
    __tablename__ = "services"

    id_service = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def __init__(self, desc, name, valor):
        self.desc = desc
        self.name = name
        self.valor = valor

class ParkingService(db.Model):
    __tablename__ = "parking_services"

    id = db.Column(db.Integer, primary_key=True)
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment")) 
    fk_services = db.Column(db.Integer, db.ForeignKey("services.id_service"))
    qtdDias = db.Column(db.Integer)
    ic_active = db.Column(db.Boolean)

    service = db.relationship("Service", foreign_keys=fk_services)
    establishment = db.relationship("Establishment", foreign_keys=fk_establishments)

    def __init__(self, fk_establishments, fk_services,qtdDias,ic_active):
        self.fk_establishments = fk_establishments
        self.fk_services = fk_services
        self.qtdDias = qtdDias
        self.ic_active = ic_active

class ScheduledRents(db.Model):
    __tablename__ = "scheduled_rents"

    id_scheduled = db.Column(db.Integer, primary_key=True)
    fk_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    fk_establishments = db.Column(db.Integer, db.ForeignKey("establishments.id_establishment"))
    start_scheduled = db.Column(db.DateTime, nullable=True)
    end_scheduled = db.Column(db.DateTime, nullable=True)
    completed_schedule = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", foreign_keys=fk_user)
    establishments = db.relationship("Establishment", foreign_keys=fk_establishments)

    def __init__(self, fk_user,fk_establishments, start_scheduled,end_scheduled):
        self.fk_user = fk_user
        self.start_scheduled = start_scheduled
        self.end_scheduled = end_scheduled
        self.fk_establishments = fk_establishments


class ServicesRentalScheduled(db.Model):
    __tablename__ = "services_rental_scheduled"

    id = db.Column(db.Integer, primary_key=True)
    fk_sheduled = db.Column(db.Integer, db.ForeignKey("scheduled_rents.id_scheduled"))
    fk_service = db.Column(db.Integer, db.ForeignKey("services.id_service")) 

    service = db.relationship("Service", foreign_keys=fk_service)
    scheduled = db.relationship("ScheduledRents", foreign_keys=fk_sheduled)

    def __init__(self, fk_sheduled,fk_service):
        self.fk_sheduled = fk_sheduled
        self.fk_service = fk_service

    
class Rent_Service(db.Model):
    __tablename__ = "services_rental"

    id_service_rent = db.Column(db.Integer, primary_key=True)
    fk_rent = db.Column(db.Integer, db.ForeignKey("rents.id_rent")) 
    fk_service = db.Column(db.Integer, db.ForeignKey("services.id_service")) 
    status = db.Column(db.Boolean, nullable=True)
    description = db.Column(db.String(500), nullable=True)

    #rental = db.relationship("MonthlyLease", foreign_keys=fk_rent)
    #service = db.relationship("Service", foreign_keys=fk_service)

    def __init__(self, fk_rent, fk_service, status, desc):
        self.fk_rent = fk_rent
        self.fk_service = fk_service
        self.status = status
        self.desc = desc

class Gate_Status(db.Model):
    __tablename__ = "gate_status"

    id = db.Column(db.Integer, primary_key=True)
    ic_open = db.Column(db.Integer)
    last_modified_date = db.Column(db.DateTime)

    def __init__(self, id, ic_open, last_modified_date):
        self.id = id
        self.ic_open = ic_open
        self.last_modified_date = last_modified_date

class Vacante_Status(db.Model):
    __tablename__ = "vacante_status"

    id = db.Column(db.Integer, primary_key=True)
    v1 = db.Column(db.Integer)
    v2 = db.Column(db.Integer)
    v3 = db.Column(db.Integer)
    last_modified_date = db.Column(db.DateTime)

    def __init__(self, id, v1, v2, v3, last_modified_date):
        self.id = id
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.last_modified_date = last_modified_date
