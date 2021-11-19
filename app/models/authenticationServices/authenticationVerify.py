from app.models.repository.UserRepository import UserRepository
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user,current_user


class authenticationVerify():

    
    def verify(self,email,password):
        message = "O E-mail e ou Senha digitados estão incorretos."
        arrayJson = {"mensagem": "true"}

        user = UserRepository.getByEmail(self,email)
        if user and check_password_hash(user.password,password):
            return arrayJson
        else:
            arrayJson["mensagem"] = message
            return arrayJson