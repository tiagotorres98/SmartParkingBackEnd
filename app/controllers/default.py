#from _typeshed import OpenBinaryMode, OpenBinaryModeReading
import asyncio
import json
from datetime import date, datetime, timedelta
from re import *

from app import app, db
from app.controllers import customSession
from app.controllers.customSession import CustomSession
from app.models.arduino.arduino import Gate
from app.models.authenticationServices.authenticationVerify import \
    authenticationVerify
from app.models.checkInOutServices.checkInOut import (CheckIn, CheckOut,
                                                      PublishRating)
from app.models.homeServices.home import *
from app.models.optionsServices.options import *
from app.models.registerServices.persistRegister import PersistRegister
from app.models.repository.creditCardRepository import CreditCardRepository
from app.models.repository.historicRepository import HistoricRepository
from app.models.repository.monthlyLeaseRepository import MonthlyLeaseRepository
from app.models.repository.parkingRepository import ParkingRepository
from app.models.repository.servicesRepository import ServicesRepository
from app.models.repository.UserRepository import UserRepository
from app.models.tables import *
from app.models.validators.checkIn import CheckInByCode, CheckOutByCode
from app.models.validators.userRegisterValidator import userRegisterValidator
from flask import render_template  # método para renderizar templates HTML,
from flask import Blueprint, flash, redirect, request, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user
from flask_session import Session
from sqlalchemy.sql.expression import case
from werkzeug.security import check_password_hash, generate_password_hash
from app.controllers.management import management_page

app.secret_key = "EgcaT3Qm#a@vf8!EWV*!^nGaQmlXNcHErWN*"

app.register_blueprint(management_page)

@app.route("/")
def index():
    return "inicial"

userEmailSession = CustomSession()

########################## INICIAL PAGES #####################################
#   LOGIN PAGE
#   REGISTER PAGE
#   FORGOT PASSWORD
########################## SCREEN LOGIN ######################################
@app.route("/login", methods=['POST', 'GET'])
def login():   

    postJson = request.data
    data = json.loads(postJson)
    email       =   data['email']
    password    =   data['password']
    arrayJson = authenticationVerify().verify(email,password)
    if arrayJson["mensagem"] == "true":
        userEmailSession.setEmailUser(email)
    return json.dumps(arrayJson)
#-----------------------------------------------------------------
#------------------------USER REGISTER----------------------------
@app.route("/register", methods=['POST', 'GET'])
def registerUser():   
    
    postJson = request.data.decode('utf8')
    data = json.loads(postJson)
    
    name        =   data['name']
    cpf         =   data['cpf']
    email       =   data['email']
    address     =   data['address']
    phone       =   data['phone']
    birthday    =   data['birthday']
    sex         =   data['sex']
    password    =   data['password']

    carModelData        =   data['car']['model']
    carBrandData        =   data['car']['brand']
    carColorData        =   data['car']['color']
    carChassiData       =   data['car']['chassi']
    carRenavamData      =   data['car']['renavam']
    carPlateData       =   data['car']['plaque']
    

    birthToInsert = birthday.replace("T"," ").replace("Z","").replace(".000","")

    person          =   Person(name,birthToInsert,sex,cpf)
    user            =   User(None,email,generate_password_hash(password, method='sha256'),'costumer',1)
    car             =   Vehicle(None,carModelData,carPlateData,carColorData,carRenavamData,carChassiData,carBrandData)
    personAdress    =   Address(None,address)
    personPhone     =   Telephone(None,'Celular',phone)
    
    
    arrayJson = userRegisterValidator().verifyAllRegister(user,person,phone,car)
    if arrayJson["mensagem"] == "true":
        result =  PersistRegister().persist(person,user,car,personAdress,personPhone) 
        if result != "":
           arrayJson["mensagem"] = result
 
    return json.dumps(arrayJson)
#----------------------------------------------------------------------
########################## END OF INICIAL PAGES ##############################


############################ OPTIONS PAGES ###################################
#   OPTIONS
#   REGISTERS INFORMATION
#   MONTHLY LEASE 
#   PAYMENT MANAGEMENT
#   HISTORIC
#   LOGOUT
###############################################################################
#---------------------OPTIONS && REGISTERS INFORMATIONS------------------------

## GET USERS INFORMATION TO DISPLAY ON MAIN SCREEN
## GET USERS INFORMATION TO DISPLAY REGISTERS INFORMATIONS
@app.route("/user", methods=['GET'])
def users():
    result = UserRepository().getAllUserDataByEmail(userEmailSession.getEmailUser())
    returnJson = json.dumps(UserRepository().resultToJson(result))
    return returnJson

 #---------------------REGISTERS INFORMATIONS -> PERFIL EDIT--------------------
## UPDATE USERS DATA
@app.route("/updateUser", methods=['POST','GET'])
def updateUserData():

    postJson = request.data.decode('utf8')
    data = json.loads(postJson)

    email       =   data['email']
    address     =   data['address']
    phone       =   data['phone']
    password    =   data['password']

    carModelData        =   data['car']['model']
    carBrandData        =   data['car']['brand']
    carColorData        =   data['car']['color']


    if authenticationVerify().verify(userEmailSession.getEmailUser(),password)["mensagem"] == "true":
        result = UpdateRegister().update(email,address,phone,carModelData,carBrandData,carColorData)
    else:
        result = {"mensagem":"Senha Incorreta. Digite Novamente."}
    returnJson = json.dumps(result)
    return returnJson
#------------------------------------------------------------------------------
#----------------------------MONTHLY LEASE-------------------------------------
@app.route("/monthlyLease", methods=['GET'])
def monthlyLease():
    user = UserRepository().getAllUserDataByEmail(userEmailSession.getEmailUser())
    leases = MonthlyLeaseRepository().getByIdUser(user.User.id)
   
    returnJson = json.dumps(MonthlyLeaseRepository().returnToJson(leases))
    return returnJson

@app.route("/cancelMonthlyLease", methods=['POST','GET'])
def cancelMonthlyLease():
    postJson = request.data.decode('utf8')
    data = json.loads(postJson)

    idLease = data['idLease']
    password = data['password']

    if authenticationVerify().verify(userEmailSession.getEmailUser(),password)["mensagem"] == "true":
        result = CancelMonthlyLease.cancel(idLease)
    else:
        result = {"mensagem":"Senha Incorreta. Digite Novamente."}
    
    returnJson = json.dumps(result)

    return returnJson

#------------------------------------------------------------------------------
#---------------------------PAYMENT MANAGEMENT---------------------------------
@app.route("/creditCard", methods=['GET'])
def getCreditCard():

    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    result = CreditCardRepository().getCardByIdPerson(user.fk_person)
    creditCard = CreditCardRepository().returnToJson(result)
    returnJson = json.dumps(creditCard)
    return returnJson
 
@app.route("/removeCreditCard", methods=['POST','GET'])
def removeCreditCard():

    postJson = request.data.decode('utf8')
    data = json.loads(postJson)

    result = CreditCardServices().remove(data)

    returnJson = json.dumps(result)
    return returnJson

@app.route("/addCreditCard", methods=['POST','GET'])
def addCreditCard():

    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')
    data = json.loads(postJson)

    ownerName       = data['ownerName']
    numberCard      = data['numberCard']
    expirationDate  = data['expirationDate'].replace("T"," ").replace("Z","").replace(".000","")
    secCode         = data['secCode']

    card = CreditCard(user.fk_person,ownerName,numberCard,expirationDate,secCode,1)

    result = CreditCardServices().addCard(card)
    
    returnJson = json.dumps(result)

    return returnJson

#------------------------------------------------------------------------------
#-------------------------------HISTORIC---------------------------------------
@app.route("/historic", methods=['GET'])
def get_historic():

    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    historic = HistoricRepository().getHistoricByIdUser(user.id)
    result = HistoricRepository().returnToJson(historic)
    returnJson = json.dumps(result)
    return returnJson

#------------------------------------------------------------------------------
#---------------------------------LOGOUT---------------------------------------

## DO NOT USE ENDPOINT YET

#------------------------------------------------------------------------------
###################### END OF OPTIONS PAGES ###################################

############################ HOME PAGES #######################################
#   HOME
#   PARKING DETAILS
#   RESERVE
###############################################################################
#--------------------------------HOME------------------------------------------
@app.route("/parkingLots", methods=['GET'])
def parking_lots():   
    parkingsFinal = []
    parkingsRepo = ParkingRepository().getAllParkings()
    parkingsJson = ParkingRepository().returnToJson(parkingsRepo)
    for parking in parkingsJson:
        services = ServicesRepository().getServicesByEstablishments(parking['id'])
        parking['services_available'] = ServicesRepository().returnToJson(services)
        parkingsFinal.append(parking)

    returnJson = json.dumps(parkingsFinal)
    return returnJson
#----------------------------PARKING DETAILS-----------------------------------
@app.route("/parkingLotsById", methods=['GET'])
def parking_lots_id():   
    id_establishment = request.args.get('id_estabelecimento')
    parkingsRepo = ParkingRepository().getAllParkingsByIdParking(id_establishment)
    parkingsJson = ParkingRepository().returnToJson(parkingsRepo)
    for parking in parkingsJson:
        services = ServicesRepository().getServicesByEstablishments(parking['id'])
        parking['services_available'] = ServicesRepository().returnToJson(services)

    returnJson = json.dumps(parkingsJson[0])
    return returnJson
#-------------------------------RESERVE----------------------------------------

# NO MONTHLY LEASE
@app.route("/scheduleRents", methods=['POST','GET'])
def scheduleRents():   

    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')
    data = json.loads(postJson)


    reserveStart        = data['id_establishment']
    reserveStart        = datetime.today() #data['reserve_start'].replace("T"," ").replace("Z","").replace(".000","")
    reserveEnd          = datetime.today() + timedelta(minutes=15) #data['reserve_end'].replace("T"," ").replace("Z","").replace(".000","")
    servicesSelected    = data['servicesSelected']

    sheduledLease = ScheduledRents(user.id,data['id_establishment'],reserveStart,reserveEnd)

    result = AddSheduledLease().add(sheduledLease,servicesSelected)

    returnJson = json.dumps(result)
    return returnJson

@app.route("/addMonthlyLease", methods=['POST','GET'])
def addMonthlyLease():

    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')
    data = json.loads(postJson)

    id_establishment    = data['id_establishment']
    start_lease         = data['start_lease'].replace("T"," ").replace("Z","").replace(".000","")
    end_lease           = data['end_lease'].replace("T"," ").replace("Z","").replace(".000","")
    id_card             = data['creditCard']['id_card']
    cardDefault         = data['creditCard']['asDefault']

    monthlyLease = MonthlyLease(user.id,id_establishment,id_card,start_lease,end_lease)

    result = AddMonthlyLease().add(monthlyLease,int(cardDefault))

    returnJson = json.dumps(result)
    return returnJson
#------------------------------------------------------------------------------
########################### END OF HOME PAGES #################################

####################### QRCODE AND NUMBERCODE PAGES ###########################
#   SCAN QRCODE TO ENTER
#   TYPE CODE TO ENTER
#   SCAN QRCODE TO EXIT
#   TYPE CODE TO EXIT
#   RATING PAGE
###############################################################################
#------------------------- SCAN QRCODE TO ENTER -------------------------------
#------------------------------------------------------------------------------
#------------------------- TYPE CODE TO ENTER ---------------------------------
@app.route("/codeToEnter", methods=['POST','GET'])
def codeToEnter():
    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')
    
    checkIn = CheckInByCode().check(postJson,user.id)
    result = checkIn

    if checkIn["mensagem"] == "true":
        result = CheckIn().addRent(user)

    if result["mensagem"] == "true":
        asyncio.run(gate())

    returnJson = json.dumps(result)
    return returnJson

#------------------------------------------------------------------------------
#------------------------- SCAN QRCODE TO EXIT --------------------------------
#------------------------------------------------------------------------------
#------------------------- TYPE CODE TO EXIT ----------------------------------
@app.route("/codeToExit", methods=['POST','GET'])
def codeToExit():
    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')
    
    checkOut = CheckOutByCode().check(postJson,user.id)
    result = checkOut

    if checkOut["mensagem"] == "true":
        result  = CheckOut().endRent(user)

    returnJson = json.dumps(result)
    return returnJson

#------------------------------------------------------------------------------
#------------------------- TYPE CODE TO EXIT ----------------------------------
@app.route("/rating", methods=['POST','GET'])
def rating():
    user = UserRepository().getByEmail(userEmailSession.getEmailUser())
    postJson = request.data.decode('utf8')

    result = PublishRating().publish(user,postJson)

    returnJson = json.dumps(result)
    return returnJson
#------------------------------------------------------------------------------

################################# ARDUINO #####################################
#   ARDUINO
###############################################################################

async def gate():
    gateOpen()
    await asyncio.sleep(10)
    gateClose()

@app.route("/gateOpen")
def gateOpen():
    Gate().open()
    return "Aberto"

@app.route("/gateClose")
def gateClose():
    Gate().close()
    return "Fechado"

############################ FILTER PAGES #######################################
#   FILTER
#   FILTER-RESULT
#################################################################################
#---------------------------------- FILTER --------------------------------------
@app.route("/filter",methods=['POST','GET'])
def filter():
    postJson =  request.args.get('filter')
    data = json.loads(postJson)

    user_avaliation = data["user_avaliation"]
    minValue = data["minValue"]
    maxValue = data["maxValue"]
    parkingNameSearch = data["parkingNameSearch"]

    parkings = ParkingRepository().getByFilter(user_avaliation,minValue,maxValue,parkingNameSearch)
    result = ParkingRepository().returnToJson(parkings)
 
    returnJson = json.dumps(result)
    return returnJson
#--------------------------------------------------------------------------------

