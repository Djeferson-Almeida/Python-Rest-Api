import hmac
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt
from blacklist import BLACKLIST

argumentos = reqparse.RequestParser()
argumentos.add_argument('login',type=str,required = True, help = "The field 'login' cannot be blank")
argumentos.add_argument('password',type=str,required = True, help = "The field 'password' cannot be blank")
argumentos.add_argument('ativado',type= bool)

class User(Resource):

    def get(self,user_id):
        user = UserModel.find_user(user_id)
        try:
            if user:
                return user.json()
        except:
            {'message': 'An error as occurred when try to find a user'},500
        return {'message': 'User not found'},404
    @jwt_required()
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
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The login '{dados['login']}' already exists."}
        
        user = UserModel(**dados)
        user.ativado = False
        user.save_user()
        return {'message': 'User created sucessfully!'},201
        
class UserLogin(Resource):
    @classmethod
    def post(cls):

        dados = argumentos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if user and hmac.compare_digest(user.password,dados['password']):
            if user.ativado:
                access_token = create_access_token(identity=str(user.user_id))
                return {'access_token': access_token},200
            return {'message': 'User not confirmed'},400
        return {'message': 'The username or password is incorrect.'},401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
    
class UserConfirm(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User id '{}' not found.".format(user_id)},404
        user.ativado = True
        user.save_user()
        return {"message":"User id '{}' confirmed successfully.".format(user_id)},200

