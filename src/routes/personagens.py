from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.rpg_models import Personagem

personagens_bp = Blueprint('personagens', __name__)

@personagens_bp.route('/personagens', methods=['POST'])
def create_personagem():
    try:
        data = request.get_json()
        new_personagem = Personagem(
            campanha_id=data['campanha_id'],
            nome=data['nome'],
            classe=data.get('classe'),
            nivel=data.get('nivel'),
            pontos_vida=data.get('pontos_vida')
        )
        db.session.add(new_personagem)
        db.session.commit()
        return jsonify({'message': 'Personagem criado com sucesso!', 'personagem': new_personagem.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personagens_bp.route('/personagens', methods=['GET'])
def get_personagens():
    try:
        campanha_id = request.args.get('campanha_id')
        if campanha_id:
            personagens = Personagem.query.filter_by(campanha_id=campanha_id).all()
        else:
            personagens = Personagem.query.all()
        return jsonify({'personagens': [personagem.to_dict() for personagem in personagens]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personagens_bp.route('/personagens/<int:id>', methods=['GET'])
def get_personagem(id):
    try:
        personagem = Personagem.query.get_or_404(id)
        return jsonify(personagem.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personagens_bp.route('/personagens/<int:id>', methods=['PUT'])
def update_personagem(id):
    try:
        personagem = Personagem.query.get_or_404(id)
        data = request.get_json()
        personagem.nome = data.get('nome', personagem.nome)
        personagem.classe = data.get('classe', personagem.classe)
        personagem.nivel = data.get('nivel', personagem.nivel)
        personagem.pontos_vida = data.get('pontos_vida', personagem.pontos_vida)
        db.session.commit()
        return jsonify({'message': 'Personagem atualizado com sucesso!', 'personagem': personagem.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@personagens_bp.route('/personagens/<int:id>', methods=['DELETE'])
def delete_personagem(id):
    try:
        personagem = Personagem.query.get_or_404(id)
        db.session.delete(personagem)
        db.session.commit()
        return jsonify({'message': 'Personagem deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

