from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ =  'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.string(40))
    senha = banco.Column(banco.string(40))

    def __init__(self,login,senha):
        self.login = login
        self.senha = senha

    def json(self):
        return{
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_user(self):
        banco.session.merge(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)      
        banco.session.commit() 



    

