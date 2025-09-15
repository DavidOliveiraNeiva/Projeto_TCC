from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.rpg_models import HistoricoSessao

historico_sessoes_bp = Blueprint('historico_sessoes', __name__)

@historico_sessoes_bp.route('/historico-sessoes', methods=['POST'])
def create_historico_sessao():
    try:
        data = request.get_json()
        data_sessao = datetime.strptime(data['data_sessao'], '%Y-%m-%d').date()
        new_historico = HistoricoSessao(
            campanha_id=data['campanha_id'],
            data_sessao=data_sessao,
            historico=data.get('historico')
        )
        db.session.add(new_historico)
        db.session.commit()
        return jsonify({'message': 'Histórico de sessão criado com sucesso!', 'historico': new_historico.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@historico_sessoes_bp.route('/historico-sessoes', methods=['GET'])
def get_historico_sessoes():
    try:
        campanha_id = request.args.get('campanha_id')
        if campanha_id:
            historicos = HistoricoSessao.query.filter_by(campanha_id=campanha_id).order_by(HistoricoSessao.data_sessao.desc()).all()
        else:
            historicos = HistoricoSessao.query.order_by(HistoricoSessao.data_sessao.desc()).all()
        return jsonify({'historicos': [historico.to_dict() for historico in historicos]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@historico_sessoes_bp.route('/historico-sessoes/<int:id>', methods=['GET'])
def get_historico_sessao(id):
    try:
        historico = HistoricoSessao.query.get_or_404(id)
        return jsonify(historico.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@historico_sessoes_bp.route('/historico-sessoes/<int:id>', methods=['PUT'])
def update_historico_sessao(id):
    try:
        historico = HistoricoSessao.query.get_or_404(id)
        data = request.get_json()
        if 'data_sessao' in data:
            historico.data_sessao = datetime.strptime(data['data_sessao'], '%Y-%m-%d').date()
        historico.historico = data.get('historico', historico.historico)
        db.session.commit()
        return jsonify({'message': 'Histórico de sessão atualizado com sucesso!', 'historico': historico.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@historico_sessoes_bp.route('/historico-sessoes/<int:id>', methods=['DELETE'])
def delete_historico_sessao(id):
    try:
        historico = HistoricoSessao.query.get_or_404(id)
        db.session.delete(historico)
        db.session.commit()
        return jsonify({'message': 'Histórico de sessão deletado com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

