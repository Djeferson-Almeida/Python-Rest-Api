from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable = False, unique = True)
    password = banco.Column(banco.String(40))
    ativado = banco.Column(banco.Boolean, default = False)

    def __init__(self, login, password,ativado):
        self.login = login
        self.password = password
        self.ativado = ativado

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




    

