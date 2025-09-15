from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.rpg_models import Item

itens_bp = Blueprint('itens', __name__)

@itens_bp.route('/itens', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        new_item = Item(
            personagem_id=data['personagem_id'],
            nome_item=data['nome_item'],
            descricao=data.get('descricao')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item criado com sucesso!', 'item': new_item.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itens_bp.route('/itens', methods=['GET'])
def get_itens():
    try:
        personagem_id = request.args.get('personagem_id')
        if personagem_id:
            itens = Item.query.filter_by(personagem_id=personagem_id).all()
        else:
            itens = Item.query.all()
        return jsonify({'itens': [item.to_dict() for item in itens]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itens_bp.route('/itens/<int:id>', methods=['GET'])
def get_item(id):
    try:
        item = Item.query.get_or_404(id)
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itens_bp.route('/itens/<int:id>', methods=['PUT'])
def update_item(id):
    try:
        item = Item.query.get_or_404(id)
        data = request.get_json()
        item.nome_item = data.get('nome_item', item.nome_item)
        item.descricao = data.get('descricao', item.descricao)
        db.session.commit()
        return jsonify({'message': 'Item atualizado com sucesso!', 'item': item.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@itens_bp.route('/itens/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

