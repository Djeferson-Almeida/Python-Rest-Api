from sql_alchemy import banco
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estado', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

def normalize_path_params(cidade=None, estado=None, estrelas_min=0, estrelas_max=5,
                          diaria_min=0, diaria_max=1000, limit=50, offset=0, **dados):
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'estado': estado,
            'limit': limit,
            'offset': offset
        }
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }

class Hoteis(Resource):
    def get(self):
        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        query = HotelModel.query.filter(
            HotelModel.estrelas >= parametros['estrelas_min'],
            HotelModel.estrelas <= parametros['estrelas_max'],
            HotelModel.diaria >= parametros['diaria_min'],
            HotelModel.diaria <= parametros['diaria_max']
        )

        if parametros.get('cidade'):
            query = query.filter_by(cidade=parametros['cidade'])
        if parametros.get('estado'):
            query = query.filter_by(estado=parametros['estado'])

        hoteis = query.limit(int(parametros['limit'])).offset(int(parametros['offset'])).all()
        return {'hoteis': [hotel.json() for hotel in hoteis]}, 200

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank")
    argumentos.add_argument('estado', type=str, required=True, help="The field 'estado' cannot be left blank")
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': f'Hotel with ID "{hotel_id}" not found.'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'hotel_id "{hotel_id}" already exists.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error occurred trying to save the hotel.'}, 500
        return hotel.json(), 201

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error occurred trying to delete the hotel.'}, 500
            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found.'}, 404
