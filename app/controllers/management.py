import json
import re
import sqlite3

from sqlalchemy.sql.sqltypes import DateTime
from app import app, db
from app.models.checkInOutServices.checkInOut import CheckOut
from app.models.repository.balanceRepository import BalanceRepository
from app.models.repository.historicRepository import HistoricRepository
from app.models.repository.parkingRepository import ParkingRepository
from app.models.repository.rentsRepository import RentsRepository
from app.models.repository.servicesRepository import ServicesRepository
from app.models.repository.vacanciesSensorsRepository import \
    VacanciesSensorsRepository
from flask import render_template  # método para renderizar templates HTML,
from flask import Blueprint, flash, redirect, request, session, url_for
from app.models.repository.ratingRepository import RatingRepository
from app.models.tables import *
from app.models.parkingManagerServices.parkingManager import ServicesData,OpeningHours
from chatterbot import ChatBot
from sqlalchemy.engine import Connection
from datetime import datetime, timedelta
from sqlalchemy import cast, Date,func,extract
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer
from spacy.cli import download

management_page = Blueprint('management_page', __name__,
                        template_folder='templates')

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

#download("en_core_web_sm")
bot = ChatBot('Lucão',storage_adapter='chatterbot.storage.SQLStorageAdapter',tagger_language=ENGSM,
database_uri='sqlite:///db.sqlite3')
bot.set_trainer(ChatterBotCorpusTrainer)
#trainer = ChatterBotCorpusTrainer(bot)
#trainer.train("./conversa.corpus.json")
#bot.train("chatterbot.corpus.portuguese.greetings")
bot.train("chatterbot.corpus.portuguese.conversa")

########################## PARKING MONITORING ###############################
#   PARKING DETAILS
#   USER RATINGS
#   VACANCIES STATUS
#############################################################################
#-----------------------------PARKING DETAILS--------------------------------
@app.route("/getParkingVacancies",methods=['GET'])
def getParkingMonitorVacancies():
    result = VacanciesSensorsRepository().getSensorsStatus()
    returnJson = VacanciesSensorsRepository().resultToJson(result)


    return json.dumps(returnJson)
#----------------------------------------------------------------------------
#------------------------------ USER RATINGS --------------------------------
@app.route("/getParkingMonitorResume",methods=['GET'])
def getParkingMonitorResume():

    qtdRent = 0
    qtdServices = 0
    time = 0
    avgTime = 0
    yesterdayQtdRent = 0
    yesterdayQtdServices = 0
    yesterdayAvgTime = 0
    avgTimeDiff=0

    rent = RentsRepository().getByDate(1,datetime.today())
    rentYesterday = RentsRepository().getByDate(1,datetime.today() - timedelta(days=1))

    for r in rent:
        qtdRent += 1
        services = ServicesRepository().getByRentId(r.id_rent)
        for s in services:
            qtdServices +=1
        time += (r.exit_time - r.entry_time).total_seconds()

    if qtdRent > 0: 
        avgTime = time / qtdRent

    for r in rentYesterday:
        yesterdayQtdRent += 1
        services = ServicesRepository().getByRentId(r.id_rent)
        for s in services:
            yesterdayQtdServices +=1
        time += (r.exit_time - r.entry_time).total_seconds()

    if yesterdayQtdRent > 0: 
        yesterdayAvgTime = time / yesterdayQtdRent

    if avgTime > yesterdayAvgTime:
        avgTimeDiff = avgTime - yesterdayAvgTime 
    elif  yesterdayAvgTime > avgTime:
        avgTimeDiff = yesterdayAvgTime - avgTime
    else:
        avgTimeDiff = yesterdayAvgTime - avgTime
    

    if yesterdayAvgTime > avgTime:
        yesterdayAvgTime = "true"
    elif yesterdayAvgTime == avgTime:
        yesterdayAvgTime = "same"
    else:
        yesterdayAvgTime = "false"


    return json.dumps({
        "qtdRent":qtdRent,
        "qtdServices":qtdServices,
        "avgTime":str(timedelta(seconds=avgTime)),
        "yesterdayQtdRent":yesterdayQtdRent,
        "yesterdayQtdServices":yesterdayQtdServices,
        "yesterdayAvgTimeBigger":yesterdayAvgTime,
        "yesterdayAvgTimeDiference":str(timedelta(seconds=avgTimeDiff))
        },)
#-----------------------------------------------------------------------------
#------------------------------ VACANCIES STATUS------------------------------
@app.route("/getVacanciesStatus",methods=['GET'])
def getVacanciesStatus():

    result = VacanciesSensorsRepository().getSensorsStatus()
    returnJson = VacanciesSensorsRepository().resultToJsonVacancies(result)

    return json.dumps(returnJson)
#-----------------------------------------------------------------------------
########################## END OF PARKING MONITORING #########################

########################## VACANCY DETAILS ###################################
#   USER DATA
#   HISTORIC
#   CANCEL VACANCY
##############################################################################
#------------------------------ USER DATA -----------------------------------
@app.route("/getVacancieMgn",methods=['GET'])
def getVacancieMgn():
    postJson = request.args.get('id_estabelecimento')
    data = json.loads(postJson)
    
    repo = RentsRepository().getById(data)
    returnJson = RentsRepository().returnJson(repo)
    return json.dumps(returnJson)
#-----------------------------------------------------------------------------
#------------------------------ HISTORIC -------------------------------------
@app.route("/historicMgn",methods=['POST','GET'])
def historicMgn():
    repo = HistoricRepository().getHistoricByIdEstablishment(1)
    returnJson = HistoricRepository().returnToJsonVacancyDetails(repo)
    return json.dumps(returnJson)
#------------------------------ HISTORIC -------------------------------------
@app.route("/cancelVacancy",methods=['POST','GET'])
def cancelVacancy():
    postJson = request.data
    data = json.loads(postJson)

    rent = RentsRepository().getJustRentById(data)
    result = CheckOut().endRentService(rent)

    return json.dumps(result)
###################### END VACANCY DETAILS ###################################

########################## PARKING MANAGER ###################################
#   ADD SERVICES
#   UPDATE SERVICES STATUS
#   ACTIVE SERVICES
#   DATETIME OPENING 
##############################################################################
#------------------------ ADD SERVICES ---------------------------------------
@app.route("/addParkingService",methods=['POST','GET'])
def addParkingService():
    postJson = request.data
    data = json.loads(postJson)
    
    serviceName = data["serviceName"]
    serviceQtdDay = data["serviceQtdDay"]
    serviceValue = data["serviceValue"]

    service = Service(serviceName,serviceName,serviceValue)
    parkingService = ParkingService(1,None,serviceQtdDay,True)

    result = ServicesData().addService(service,parkingService)

    jsonReturn = result
    return json.dumps(jsonReturn)
#-----------------------------------------------------------------------------
#------------------------ UPDATE SERVICES ---------------------------------------
@app.route("/updateParkingService",methods=['POST','GET'])
def updateParkingService():
    postJson = request.data
    data = json.loads(postJson)
    
    service_id = data["service_id"]
    service_name = data["service_name"]
    service_price = data["service_price"]
    active = data["active"]

    jsonReturn = ServicesData().updateService(service_id,active)
    return json.dumps(jsonReturn)
#-----------------------------------------------------------------------------
#------------------------ ACTIVE SERVICES ------------------------------------
@app.route("/getServicesMgnActive",methods=['GET'])
def getServicesMgn2():
    repo = ServicesRepository().getAllServicesByEstablishments(1)
    returnJson = ServicesRepository().returnToJson(repo)
    return json.dumps(returnJson)
#-----------------------------------------------------------------------------
#-------------------------DATETIME OPENING -----------------------------------
@app.route("/getOpeningHours",methods=['GET'])
def getOpeningHours():
    repo = ParkingRepository().getAllParkingsByIdParking(1)
    returnJson = ParkingRepository().returnToJsonParkingManager(repo)
    return json.dumps(returnJson)
#-----------------------------------------------------------------------------
#----------------------- ALTER DATETIME OPENING ------------------------------
@app.route("/updateOpeningHours",methods=['POST','GET'])
def updateOpeningHours():

    postJson = request.data
    data = json.loads(postJson)

    open            =     data["open"]
    close           =     data["close"]
    day_week_init   =     data["day_week_init"]
    day_week_end    =     data["day_week_end"]

    returnJson = OpeningHours().updateOpening(open,close,day_week_init,day_week_end,)
    return json.dumps(returnJson)
#-----------------------------------------------------------------------------
########################## LEASE MANAGEMENT ###################################
#   HISTORIC DETAILS
##############################################################################
#--------------------------- HISTORIC DETAILS --------------------------------
###DEPRECIATED
@app.route("/historicMgnDetail",methods=['POST','GET'])
def historicMgnDetail():
    repo = HistoricRepository().getHistoricByIdEstablishment(1)
    returnJson = HistoricRepository().returnToJsonVacancyDetails2(repo)
    return json.dumps(returnJson)
#------------------------------------------------------------------------------
################################ LEASE MANAGEMENT #############################
#   DAILY BALANCE
#   MONTHLY BALANCE
##############################################################################
#--------------------------- DAILY BALANCE ------------------------------------
@app.route("/balanceFiveDays",methods=['POST','GET'])
def balanceFiveDays():
    try:
        postJson = request.args.get('date')
        date = datetime.strptime(postJson.split("T")[0], '%Y-%m-%d')
        result = BalanceRepository().balanceFiveDays(date)
        jsonR = {
            "today": result[0],
            "last1day": result[1],
            "last2day": result[2],
            "last3day": result[3],
            "last4day": result[4]
        }
        print(jsonR)
        return json.dumps(jsonR)
    except:
        jsonR = {
            "today": 0,
            "last1day": 0,
            "last2day": 0,
            "last3day": 0,
            "last4day": 0
        }
        print(jsonR)
        return json.dumps(jsonR)

#--------------------------------------------------------------------------------
#--------------------------- MONTHLY BALANCE ------------------------------------
@app.route("/balanceFiveMonths",methods=['POST','GET'])
def balanceFiveMonths():
    try:
        postJson = request.args.get('json')
        get = json.loads(postJson)
        print(get)
        result = BalanceRepository().balanceFiveMonths(get)

        jsonR = {
            "now": result[0],
            "last1month": result[1],
            "last2month": result[2],
            "last3month": result[3],
            "last4month": result[4],
            "last5month": result[5],
            "last6month": result[6],
            "last7month": result[7],
            "last8month": result[8],
            "last9month": result[9],
            "last10month": result[10],
            "last11month": result[11],
            "currentMonth": result[12]
        }
        return json.dumps(jsonR)
    except:
        jsonR = {
            "now":0,
            "last1month": 0,
            "last2month": 0,
            "last3month": 0,
            "last4month": 0,
            "last5month": 0,
            "last6month": 0,
            "last7month": 0,
            "last8month": 0,
            "last9month": 0,
            "last10month": 0,
            "last11month": 0,
            "currentMonth": 0
        }
        return json.dumps(jsonR)
        
#--------------------------------------------------------------------------------
#--------------------------- WEEK BALANCE ------------------------------------
@app.route("/balanceWeek",methods=['POST','GET'])
def balanceWeek():
    postJson = request.args.get('json')
    get = json.loads(postJson)
    result = BalanceRepository().balanceWeek(get)
    weekTotal = 0

    for r in result:
        weekTotal += r

    jsonR = {
        "day1":result[0],
        "day2":result[1],
        "day3":result[2],
        "day4":result[3],
        "day5":result[4],
        "day6":result[5],
        "day7":result[6],
        "total":weekTotal,
        "today":result[7]
    }
    return json.dumps(jsonR)
############################## END OF LEASE MANAGEMENT ########################

################################ REGISTRATION #############################
#   INFO
#   UPDATE INFO
##############################################################################
#---------------------------------- INFO -------------------------------------
@app.route("/parkingData",methods=['POST','GET'])
def parkingData():

    parking = ParkingRepository().getAllParkingsByIdParking(1)
    jsonR = ParkingRepository().returnToJsonParkingManagerRegister(parking)

    return json.dumps(jsonR)
#-----------------------------------------------------------------------------
################################ IA ##########################################
#   IA
##############################################################################
#---------------------------IA------------------------------------------------
@app.route("/ia",methods=['POST','GET'])
def IA():
    postJson = request.data
    data = json.loads(postJson)

    question = data["question"]

    print(postJson)

    result = bot.get_response(question)
    
    return json.dumps(str(result))
#-----------------------------------------------------------------------------------