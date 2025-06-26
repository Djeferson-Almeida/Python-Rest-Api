from sql_alchemy import banco
from flask import url_for, request
import requests
import os

MAILGUN_DOMAIN = "sandbox23fa5b96fb754a1eadaa9e4edf0ab1af.mailgun.org"
MAILGUN_API_KEY = "key-6f24de2761f4c96274ade73961b9a8cd-a1dad75f-e1d7da7e"
FROM_TITLE = "NO-REPLY"
FROM_EMAIL = "no-reply@restapi.com"

class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable = False, unique = True)
    password = banco.Column(banco.String(40))
    ativado = banco.Column(banco.Boolean, default = False)

    def __init__(self, login, password, email, ativado):
        self.login = login
        self.password = password
        self.email = email
        self.ativado = ativado

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return requests.post(
            f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
            auth=("api", os.getenv('MAILGUN_API_KEY', MAILGUN_API_KEY)),
            data={
                "from": f'{FROM_TITLE} <{FROM_EMAIL}>',
                "to": self.email,
                "subject": "Confirmação de Cadastro",
                "text": f'Confirme seu cadastro clicando no link a seguir: {link}',
                "html": f'<html><p>Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a></p></html>'
            }
        )
  		    



    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login,
            'ativado': self.ativado
        }

    @classmethod
    def find_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()


    def save_user(self):
        banco.session.merge(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)      
        banco.session.commit() 



    

