from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.rpg_models import Missao

missoes_bp = Blueprint('missoes', __name__)

@missoes_bp.route('/missoes', methods=['POST'])
def create_missao():
    try:
        data = request.get_json()
        new_missao = Missao(
            campanha_id=data['campanha_id'],
            nome_missao=data['nome_missao'],
            tipo_missao=data.get('tipo_missao'),
            descricao=data.get('descricao'),
            objetivo=data.get('objetivo'),
            premio=data.get('premio')
        )
        db.session.add(new_missao)
        db.session.commit()
        return jsonify({'message': 'Missão criada com sucesso!', 'missao': new_missao.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@missoes_bp.route('/missoes', methods=['GET'])
def get_missoes():
    try:
        campanha_id = request.args.get('campanha_id')
        if campanha_id:
            missoes = Missao.query.filter_by(campanha_id=campanha_id).all()
        else:
            missoes = Missao.query.all()
        return jsonify({'missoes': [missao.to_dict() for missao in missoes]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@missoes_bp.route('/missoes/<int:id>', methods=['GET'])
def get_missao(id):
    try:
        missao = Missao.query.get_or_404(id)
        return jsonify(missao.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@missoes_bp.route('/missoes/<int:id>', methods=['PUT'])
def update_missao(id):
    try:
        missao = Missao.query.get_or_404(id)
        data = request.get_json()
        missao.nome_missao = data.get('nome_missao', missao.nome_missao)
        missao.tipo_missao = data.get('tipo_missao', missao.tipo_missao)
        missao.descricao = data.get('descricao', missao.descricao)
        missao.objetivo = data.get('objetivo', missao.objetivo)
        missao.premio = data.get('premio', missao.premio)
        db.session.commit()
        return jsonify({'message': 'Missão atualizada com sucesso!', 'missao': missao.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@missoes_bp.route('/missoes/<int:id>', methods=['DELETE'])
def delete_missao(id):
    try:
        missao = Missao.query.get_or_404(id)
        db.session.delete(missao)
        db.session.commit()
        return jsonify({'message': 'Missão deletada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

