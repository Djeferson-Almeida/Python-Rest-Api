class HotelModel:
    def __init__(self, hotel_id, nome, estrelas, diaria, estado, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.estado = estado
        self.cidade = cidade      
   
    def json(self):
        return{
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'estado': self.estado,
            'cidade': self.cidade
        } 
