from flask_restful import Resource, reqparse

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
        return {'hoteis': hoteis}
    

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
   
     def get(self,hotel_id):
       hotel = Hotel.find_hotel(hotel_id)
       if hotel:
            return hotel
       return {'message': 'hotel not found'}, 404

     def post(self,hotel_id):

       dados = Hotel.argumentos.parse_args()

       novo_hotel = {
           'hotel_id': hotel_id,
           'nome': dados['nome'],
           'estrelas': dados['estrelas'],
           'diaria': dados['diaria'],
           'estado': dados['estado'],
           'cidade': dados['cidade']
       }
       hoteis.append(novo_hotel)
       return novo_hotel,200
   
     def put (self,hotel_id):
       dados = Hotel.argumentos.parse_args()

       novo_hotel = {'hotel_id': hotel_id, **dados }
       hotel = Hotel.find_hotel(hotel_id)
       if Hotel:
           hotel.update(novo_hotel)
           return novo_hotel, 200
       hoteis.append(novo_hotel)
       return novo_hotel, 201
     def delete (self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]  
        return {'message':  'Hotel deleted'}
   



       
