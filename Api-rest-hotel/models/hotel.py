from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key = True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    estado = banco.Column(banco.String(40))
    cidade =banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer,banco.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, nome, estrelas, diaria, estado, cidade,site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.estado = estado
        self.cidade = cidade      
        self.site_id = site_id
   
    def json(self):
        return{
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'estado': self.estado,
            'cidade': self.cidade,
            'site_id': self.site_id
        } 
    
    @classmethod
    def find_hotel(cls, hotel_id):
        return cls.query.filter_by(hotel_id=hotel_id).first()

    def save_hotel(self):
        banco.session.merge(self)
        banco.session.commit()

    def update_hotel(self, **dados):
        self.nome = dados.get('nome', self.nome)
        self.estrelas = dados.get('estrelas', self.estrelas)
        self.diaria = dados.get('diaria', self.diaria)
        self.estado = dados.get('estado', self.estado)
        self.cidade = dados.get('cidade', self.cidade)       
    def delete_hotel(self):
        banco.session.delete(self)      
        banco.session.commit() 