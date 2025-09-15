from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Campanha(db.Model):
    __tablename__ = 'campanhas'
    id = db.Column(db.Integer, primary_key=True)
    nome_campanha = db.Column(db.String(255), nullable=False)
    nome_mestre = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_campanha': self.nome_campanha,
            'nome_mestre': self.nome_mestre
        }

class HistoricoSessao(db.Model):
    __tablename__ = 'historico_sessoes'
    id = db.Column(db.Integer, primary_key=True)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanhas.id'), nullable=False)
    data_sessao = db.Column(db.Date, nullable=False)
    historico = db.Column(db.Text)
    campanha = db.relationship('Campanha', backref=db.backref('historico_sessoes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'campanha_id': self.campanha_id,
            'data_sessao': self.data_sessao.isoformat() if self.data_sessao else None,
            'historico': self.historico
        }

class Personagem(db.Model):
    __tablename__ = 'personagens'
    id = db.Column(db.Integer, primary_key=True)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanhas.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    classe = db.Column(db.String(255))
    nivel = db.Column(db.Integer)
    pontos_vida = db.Column(db.Integer)
    campanha = db.relationship('Campanha', backref=db.backref('personagens', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'campanha_id': self.campanha_id,
            'nome': self.nome,
            'classe': self.classe,
            'nivel': self.nivel,
            'pontos_vida': self.pontos_vida
        }

class Item(db.Model):
    __tablename__ = 'itens'
    id = db.Column(db.Integer, primary_key=True)
    personagem_id = db.Column(db.Integer, db.ForeignKey('personagens.id'), nullable=False)
    nome_item = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    personagem = db.relationship('Personagem', backref=db.backref('itens', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'personagem_id': self.personagem_id,
            'nome_item': self.nome_item,
            'descricao': self.descricao
        }

class Missao(db.Model):
    __tablename__ = 'missoes'
    id = db.Column(db.Integer, primary_key=True)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanhas.id'), nullable=False)
    nome_missao = db.Column(db.String(255), nullable=False)
    tipo_missao = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    objetivo = db.Column(db.Text)
    premio = db.Column(db.Text)
    campanha = db.relationship('Campanha', backref=db.backref('missoes', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'campanha_id': self.campanha_id,
            'nome_missao': self.nome_missao,
            'tipo_missao': self.tipo_missao,
            'descricao': self.descricao,
            'objetivo': self.objetivo,
            'premio': self.premio
        }

class NPC(db.Model):
    __tablename__ = 'npcs'
    id = db.Column(db.Integer, primary_key=True)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanhas.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    localizacao = db.Column(db.String(255))
    personalidade = db.Column(db.Text)
    descricao = db.Column(db.Text)
    campanha = db.relationship('Campanha', backref=db.backref('npcs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'campanha_id': self.campanha_id,
            'nome': self.nome,
            'localizacao': self.localizacao,
            'personalidade': self.personalidade,
            'descricao': self.descricao
        }

