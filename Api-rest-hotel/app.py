from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin
from flask_jwt_extended import JWTManager
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'  #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ThisIsAKey'
api = Api(app)
jwt = JWTManager(app)

banco.init_app(app)

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User,'/users/<int:user_id>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    with app.app_context():
        banco.create_all()
    app.run(debug=True)
    