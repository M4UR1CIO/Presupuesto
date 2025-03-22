from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from database.db import db
from models.presupuesto_model import Presupuesto

presupuesto_bp = Blueprint('presupuesto', __name__)

# Obtener Presupuesto
@presupuesto_bp.route('/presupuestos', methods=['GET'])
@jwt_required()
def obtener_presupuestos():
    usuario_id = get_jwt_identity()
    presupuestos = Presupuesto.query.filter_by(usuario_id=usuario_id).order_by(Presupuesto.numero_presupuesto.asc()).all()

    return jsonify([{
        "id": p.id,
        "numero_presupuesto": p.numero_presupuesto,  # Agregado
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "total": p.total,
        "fecha_creacion": p.fecha_creacion
    } for p in presupuestos]), 200


# Crear Presupuesto
@presupuesto_bp.route('/presupuestos', methods=['POST'])
@jwt_required()
def crear_presupuesto():
    usuario_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('nombre') or not data.get('total'):
        return jsonify({"msg": "Nombre y total son obligatorios"}), 400

    nuevo_presupuesto = Presupuesto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ""),
        total=data['total'],
        usuario_id=usuario_id,
        numero_presupuesto=Presupuesto.obtener_siguiente_numero(usuario_id)  # Generar número incremental
    )

    db.session.add(nuevo_presupuesto)
    db.session.commit()

    return jsonify({
        "msg": "Presupuesto creado con éxito",
        "id": nuevo_presupuesto.id,
        "numero_presupuesto": nuevo_presupuesto.numero_presupuesto
    }), 201

# Actualizar Presupuesto
@presupuesto_bp.route('/presupuestos/<int:presupuesto_id>', methods=['PUT'])
@jwt_required()
def actualizar_presupuesto(presupuesto_id):
    usuario_id = get_jwt_identity()
    presupuesto = Presupuesto.query.get(presupuesto_id)

    if not presupuesto:
        return jsonify({"msg": "Presupuesto no encontrado"}), 404

    if presupuesto.usuario_id != int(usuario_id):
        print(presupuesto.usuario_id, usuario_id)
        
        return jsonify({"msg": "No tienes permiso para modificar este presupuesto"}), 403

    data = request.get_json()
    presupuesto.nombre = data.get('nombre', presupuesto.nombre)
    presupuesto.descripcion = data.get('descripcion', presupuesto.descripcion)
    presupuesto.total = data.get('total', presupuesto.total)

    db.session.commit()
    return jsonify({"msg": "Presupuesto actualizado"}), 200

# Eliminar Presupuesto
@presupuesto_bp.route('/presupuestos/<int:presupuesto_id>', methods=['DELETE'])
@jwt_required()
def eliminar_presupuesto(presupuesto_id):
    usuario_id = get_jwt_identity()
    presupuesto = Presupuesto.query.get(presupuesto_id)

    if not presupuesto:
        return jsonify({"msg": "Presupuesto no encontrado"}), 404

    if presupuesto.usuario_id != int(usuario_id):
        return jsonify({"msg": "No tienes permiso para eliminar este presupuesto"}), 403

    # Eliminar el presupuesto
    db.session.delete(presupuesto)
    db.session.commit()

    # Recalcular los números de presupuesto
    presupuestos = Presupuesto.query.filter_by(usuario_id=usuario_id).order_by(Presupuesto.numero_presupuesto).all()
    for i, p in enumerate(presupuestos, start=1):
        p.numero_presupuesto = i

    db.session.commit()

    return jsonify({"msg": "Presupuesto eliminado y números recalculados"}), 200