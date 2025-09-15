from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.rpg_models import NPC

npcs_bp = Blueprint('npcs', __name__)

@npcs_bp.route('/npcs', methods=['POST'])
def create_npc():
    try:
        data = request.get_json()
        new_npc = NPC(
            campanha_id=data['campanha_id'],
            nome=data['nome'],
            localizacao=data.get('localizacao'),
            personalidade=data.get('personalidade'),
            descricao=data.get('descricao')
        )
        db.session.add(new_npc)
        db.session.commit()
        return jsonify({'message': 'NPC criado com sucesso!', 'npc': new_npc.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@npcs_bp.route('/npcs', methods=['GET'])
def get_npcs():
    try:
        campanha_id = request.args.get('campanha_id')
        if campanha_id:
            npcs = NPC.query.filter_by(campanha_id=campanha_id).all()
        else:
            npcs = NPC.query.all()
        return jsonify({'npcs': [npc.to_dict() for npc in npcs]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@npcs_bp.route('/npcs/<int:id>', methods=['GET'])
def get_npc(id):
    try:
        npc = NPC.query.get_or_404(id)
        return jsonify(npc.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@npcs_bp.route('/npcs/<int:id>', methods=['PUT'])
def update_npc(id):
    try:
        npc = NPC.query.get_or_404(id)
        data = request.get_json()
        npc.nome = data.get('nome', npc.nome)
        npc.localizacao = data.get('localizacao', npc.localizacao)
        npc.personalidade = data.get('personalidade', npc.personalidade)
        npc.descricao = data.get('descricao', npc.descricao)
        db.session.commit()
        return jsonify({'message': 'NPC atualizado com sucesso!', 'npc': npc.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@npcs_bp.route('/npcs/<int:id>', methods=['DELETE'])
def delete_npc(id):
    try:
        npc = NPC.query.get_or_404(id)
        db.session.delete(npc)
        db.session.commit()
        return jsonify({'message': 'NPC deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

