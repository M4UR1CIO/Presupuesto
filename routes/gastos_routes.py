from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from models.gasto_model import Gasto
from database.db import db
from models.presupuesto_model import Presupuesto

gasto_bp = Blueprint('gasto', __name__)

@gasto_bp.route('/presupuestos/<int:presupuesto_id>/gastos', methods=['GET'])
@jwt_required()
def obtener_gastos(presupuesto_id):
    usuario_id = get_jwt_identity()
    presupuesto = Presupuesto.query.get(presupuesto_id)
    if not presupuesto:
        return jsonify({"msg": "Presupuesto no encontrado"}), 404
    
    if presupuesto.usuario_id != int(usuario_id):
        return jsonify({"msg": "No tienes permiso para ver los gastos de este presupuesto"}), 403
    
    gastos = Gasto.query.filter_by(presupuesto_id=presupuesto_id).all()
    
    return jsonify([{
        "id": gasto.id,
        "descripcion": gasto.descripcion,
        "monto": gasto.monto,
        "fecha": gasto.fecha
    } for gasto in gastos]), 200

# Agregar un gasto a un presupuesto
@gasto_bp.route('/gastos', methods=['POST'])
@jwt_required()
def agregar_gasto():
    data = request.get_json()
    usuario_id = get_jwt_identity()
    presupuesto_id = data.get('presupuesto_id')
    
    presupuesto = Presupuesto.query.get(presupuesto_id)
    if not presupuesto:
        return jsonify({"msg": "Presupuesto no encontrado"}), 404
    
    if presupuesto.usuario_id != int(usuario_id):
        return jsonify({"msg": "No tienes permiso para agregar gastos a este presupuesto"}), 403
    
    nuevo_gasto = Gasto(
        descripcion=data.get('descripcion'),
        monto=data.get('monto'),
        fecha=data.get('fecha'),
        presupuesto_id=presupuesto_id
    )
    db.session.add(nuevo_gasto)
    db.session.commit()
    
    return jsonify({"msg": "Gasto agregado correctamente"}), 201

# Actualizar un gasto
@gasto_bp.route('/gastos/<int:gasto_id>', methods=['PUT'])
@jwt_required()
def actualizar_gasto(gasto_id):
    data = request.get_json()
    usuario_id = get_jwt_identity()
    gasto = Gasto.query.get(gasto_id)
    
    if not gasto:
        return jsonify({"msg": "Gasto no encontrado"}), 404
    
    presupuesto = Presupuesto.query.get(gasto.presupuesto_id)
    if presupuesto.usuario_id != int(usuario_id):
        return jsonify({"msg": "No tienes permiso para modificar este gasto"}), 403
    
    gasto.descripcion = data.get('descripcion', gasto.descripcion)
    gasto.monto = data.get('monto', gasto.monto)
    gasto.fecha = data.get('fecha', gasto.fecha)
    
    db.session.commit()
    return jsonify({"msg": "Gasto actualizado correctamente"}), 200

# Eliminar un gasto
@gasto_bp.route('/gastos/<int:gasto_id>', methods=['DELETE'])
@jwt_required()
def eliminar_gasto(gasto_id):
    usuario_id = get_jwt_identity()
    gasto = Gasto.query.get(gasto_id)
    
    if not gasto:
        return jsonify({"msg": "Gasto no encontrado"}), 404
    
    presupuesto = Presupuesto.query.get(gasto.presupuesto_id)
    if presupuesto.usuario_id != int(usuario_id):
        return jsonify({"msg": "No tienes permiso para eliminar este gasto"}), 403
    
    db.session.delete(gasto)
    db.session.commit()
    return jsonify({"msg": "Gasto eliminado correctamente"}), 200