import json
import re
from datetime import date, datetime
from operator import countOf
from app import db
from app.models.tables import Person,User
from app.models.repository.UserRepository import UserRepository
from app.models.repository.PersonRepository import PersonRepository

class userRegisterValidator:

    def verifyAllRegister(self,user,person,phone,car):
        message = ""
        arrayJson = {"mensagem": "true"}

        if self.verifyBornDate(person.birth_date) == False:
            message += "O usuario deve ter 18 anos ou mais;"

        if self.verifyExistsCPF(person.cpf) == False:    
            message += "O CPF informado já está cadastrado;"
        
        if self.validate_cpf(person.cpf) == False:    
            message += "O CPF informado é inválido;"

        if self.verifyExistsEmail(user.email) == False:    
            message += "O Email informado já está cadastrado;"
        
        if self.verifyPhone(phone) == False:    
            message += "O Telefone possui a quantidade de caracteres errada;"

        if self.verifyPlaque(car.plate) == False:    
            message += "Padrão incorreto da placa. "\
                        "Padrão antigo: AAA-0000; "\
                        "Padrão novo: AAA0A00"

        if message != "":
            arrayJson["mensagem"] = message

        return arrayJson
        
    def verifyExistsCPF(self,cpf):
        persons = PersonRepository().getByCPF(cpf)

        if persons:
            return False
        else:
            return True
    

    def verifyExistsEmail(self,email):
        users = UserRepository().getByEmail(email)

        if users:
            return False
        else:
            return True
    
    def verifyBornDate(self,date):
        today = datetime.today()
        birthDate = datetime.strptime(date.replace("T"," ").replace("Z","").replace(".000",""),"%Y-%m-%d %H:%M:%S")
        age = today.year - birthDate.year - ((today.month, today.day) <  (birthDate.month, birthDate.day))
        if age < 18:
            return False 
        else:
            return True
        
    def verifyPhone(self,phone):
        qtd = len(phone)
        if qtd < 10 and qtd > 11:
            return False

    def validate_cpf(self,cpf):
        if len(cpf) < 11:
            return False    

        if len(cpf) > 11:
            return False  
        
        if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
            return False
        
        if (cpf == '11111111111' or  cpf == '22222222222' or  
            cpf == '33333333333' or  cpf == '44444444444' or
            cpf == '55555555555' or  cpf == '66666666666' or  
            cpf == '77777777777' or  cpf == '88888888888' or
            cpf == '99999999999' or  cpf == '00000000000'):
            return False

        calc = [i for i in range(1, 10)]
        d1= (sum([int(a)*b for a,b in zip(cpf[:-2], calc)]) % 11) % 10
        d2= (sum([int(a)*b for a,b in zip(reversed(cpf[:-2]), calc)]) % 11) % 10
        return str(d1) == cpf[-2] and str(d2) == cpf[-1]

    def verifyPlaque(self,plate):
        
        if re.search(r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}',plate) != None and len(plate) == 7:
            return True
        else:
            if re.search(r'[A-Z]{3}[-][0-9]{4}',plate) != None and len(plate) == 8:
                return True
            else:
                return False
        
        