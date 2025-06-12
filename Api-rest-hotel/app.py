from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ThisIsAKey'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

banco.init_app(app)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User,'/users/<int:user_id>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites') 
api.add_resource(Site, '/sites/<string:url>')


@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_validado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

if __name__ == '__main__':
    with app.app_context():
        banco.create_all()
    app.run(debug=True)
    