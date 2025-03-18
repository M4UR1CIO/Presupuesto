from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from database.db import db
from models.user_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    # Validación de datos
    if not nombre or not email or not password:
        return jsonify({"msg": "Todos los campos son obligatorios"}), 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"msg": "El usuario ya existe"}), 400
    
    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email
    )

    nuevo_usuario.set_password(password)

    # Guardar en la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario creado exitosamente"}), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg":"Faltan Credenciales"}), 400
    
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"msg": "Credenciales inválidas"}), 401
    
    access_token = create_access_token(identity=str(usuario.id))
    refresh_token = create_refresh_token(identity=usuario.email)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@auth_bp.route('/perfil', methods=["GET"])
@jwt_required()
def perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Solo acepta el Refresh Token
def refresh_token():
    usuario_actual = get_jwt_identity()  # Extrae el usuario del refresh token
    nuevo_access_token = create_access_token(identity=usuario_actual)
    return jsonify(access_token=nuevo_access_token)