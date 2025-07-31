import hmac
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt
from blacklist import BLACKLIST

argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="The field 'login' cannot be blank")
argumentos.add_argument('password', type=str, required=True, help="The field 'password' cannot be blank")
argumentos.add_argument('email', type=str, required=True, help="The field 'email' cannot be blank")
argumentos.add_argument('ativado', type=bool, required=False)

class User(Resource):
    def get(self, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return {'message': 'User ID must be a valid integer.'}, 400

        user = UserModel.find_user(user_id)
        if user:
            try:
                return user.json(), 200
            except Exception:
                return {'message': 'An internal error occurred while fetching user data.'}, 500
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return {'message': 'User ID must be a valid integer.'}, 400

        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {'message': f'User ID:{user_id} deleted successfully.'}, 200
            except Exception:
                return {'message': 'An internal error occurred while trying to delete the user.'}, 500
        return {'message': f'User ID:{user_id} not found.'}, 404


class UserRegister(Resource):
    def post(self):
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': f"The login '{dados['login']}' already exists."}, 400

        try:
            user = UserModel(**dados)
            user.save_user()
            return {'message': 'User created successfully!'}, 201
        except Exception:
            return {'message': 'An internal error occurred while registering the user.'}, 500


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.password, dados['password']):
            if user.ativado:
                access_token = create_access_token(identity=str(user.user_id))
                return {'access_token': access_token}, 200
            return {'message': 'User not confirmed. Please check your email to confirm your account.'}, 400
        return {'message': 'Incorrect username or password.'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            jwt_id = get_jwt()['jti']
            BLACKLIST.add(jwt_id)
            return {'message': 'Logged out successfully!'}, 200
        except Exception:
            return {'message': 'An internal error occurred while trying to log out.'}, 500


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return {'message': 'User ID must be a valid integer.'}, 400

        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User with ID '{}' not found.".format(user_id)}, 404
        
        if user.ativado:
            return {"message": "User with ID '{}' is already activated.".format(user_id)}, 400

        try:
            user.ativado = True
            user.save_user()
            return {"message": "User with ID '{}' confirmed successfully.".format(user_id)}, 200
        except Exception:
            return {'message': 'An internal error occurred while confirming the user.'}, 500