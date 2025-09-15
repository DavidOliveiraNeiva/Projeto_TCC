from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.rpg_models import Campanha

campanhas_bp = Blueprint('campanhas', __name__)

@campanhas_bp.route('/campanhas', methods=['POST'])
def create_campanha():
    try:
        data = request.get_json()
        new_campanha = Campanha(
            nome_campanha=data['nome_campanha'], 
            nome_mestre=data['nome_mestre']
        )
        db.session.add(new_campanha)
        db.session.commit()
        return jsonify({'message': 'Campanha criada com sucesso!', 'campanha': new_campanha.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@campanhas_bp.route('/campanhas', methods=['GET'])
def get_campanhas():
    try:
        campanhas = Campanha.query.all()
        return jsonify({'campanhas': [campanha.to_dict() for campanha in campanhas]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@campanhas_bp.route('/campanhas/<int:id>', methods=['GET'])
def get_campanha(id):
    try:
        campanha = Campanha.query.get_or_404(id)
        return jsonify(campanha.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@campanhas_bp.route('/campanhas/<int:id>', methods=['PUT'])
def update_campanha(id):
    try:
        campanha = Campanha.query.get_or_404(id)
        data = request.get_json()
        campanha.nome_campanha = data.get('nome_campanha', campanha.nome_campanha)
        campanha.nome_mestre = data.get('nome_mestre', campanha.nome_mestre)
        db.session.commit()
        return jsonify({'message': 'Campanha atualizada com sucesso!', 'campanha': campanha.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@campanhas_bp.route('/campanhas/<int:id>', methods=['DELETE'])
def delete_campanha(id):
    try:
        campanha = Campanha.query.get_or_404(id)
        db.session.delete(campanha)
        db.session.commit()
        return jsonify({'message': 'Campanha deletada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

