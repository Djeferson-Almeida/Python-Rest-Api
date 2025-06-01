from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):

    def get(self,user_id):
        user = UserModel.find_user(user_id)
        try:
            if user:
                return user.json()
        except:
            {'message': 'An error as occurred when try to find a user'},500
        return {'message': 'User not found'},404

    def delete(self,user_id):
        user = UserModel.find_user(user_id)
        try:
            if user:
                return user.delete_user()
        except:
            {'message': 'An error as occurred when try to delete a user'},500
            return {'message':'User id:{user_id} not found'}


class UserRegister(Resource):
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('login',type=str,required = True, help = "The field 'login' cannot be blank")
        argumentos.add_argument('password',type=str,required = True, help = "The field 'password' cannot be blank")
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': 'The login {login} already exists.'}
        
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created sucessfully!'},201
        


        
