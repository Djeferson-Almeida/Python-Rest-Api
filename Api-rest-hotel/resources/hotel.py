from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.3,
        'diaria': 365.56,
        'estado': 'SC',
        'cidade': 'Santa Catarina'
    }
    ]

class Hoteis(Resource):
    def get(self):
        todos_hoteis = HotelModel.query.all()
        return {'hoteis': [hotel.json() for hotel in todos_hoteis]}

class Hotel(Resource):
     argumentos = reqparse.RequestParser()
     argumentos.add_argument('nome')
     argumentos.add_argument('estrelas')
     argumentos.add_argument('diaria')
     argumentos.add_argument('estado')
     argumentos.add_argument('cidade')

     def find_hotel(hotel_id):
       for hotel in hoteis:
           if hotel ['hotel_id'] == hotel_id:
               return hotel
       return None
   
     def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
          return hotel.json()
        return {'message': f'Hotel with ID "{hotel_id}" not found.'}, 404

     def post(self,hotel_id):
         if HotelModel.find_hotel(hotel_id):
            return {'message': f'hotel_id "{hotel_id}" already exists.'}, 400
         
         dados = Hotel.argumentos.parse_args()
         hotel = HotelModel(hotel_id,**dados)
         hotel.save_hotel()
         return hotel.json(),201
   
     def put (self,hotel_id):
         dados = Hotel.argumentos.parse_args()   
         hotel_encontrado = Hotel.find_hotel(hotel_id)


         if hotel_encontrado:
           hotel_encontrado.update_hotel(**dados)
           hotel_encontrado.save_hotel()
           return hotel_encontrado.json(), 200
         
         hotel = HotelModel(hotel_id,**dados)         
         hotel.save_hotel()
         return hotel.json(), 201
     
     def delete (self,hotel_id):
         hotel = HotelModel.find_hotel(hotel_id)
         if hotel: 
             hotel.delete_hotel()
             return {'message':  'Hotel deleted'}
         return{'message': 'Hotel not found'}, 404

