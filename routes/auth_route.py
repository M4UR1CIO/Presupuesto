from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
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

    # Crear la respuesta JSON
    response = jsonify({"msg": "Login exitoso"})

    # Guardar tokens en cookies
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

# Perfil
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

@auth_bp.route('/editar-perfil', methods=['PUT'])
@jwt_required()
def editar_perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    data = request.get_json()
    nuevo_nombre = data.get('nombre')
    nueva_password = data.get('password')
    confirmar_password = data.get('confirm_password')

    # Validación de datos
    if not nuevo_nombre:
        return jsonify({"msg": "El nombre no puede estar vacío"}), 400

    if nueva_password:
        if nueva_password != confirmar_password:
            return jsonify({"msg": "Las contraseñas no coinciden"}), 400
        usuario.set_password(nueva_password)  # Guardar nueva contraseña encriptada

    # Actualizar nombre de usuario
    usuario.nombre = nuevo_nombre

    # Guardar cambios
    db.session.commit()

    return jsonify({"msg": "Perfil actualizado exitosamente"}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Solo acepta el Refresh Token
def refresh_token():
    usuario_actual = get_jwt_identity()  # Extrae el usuario del refresh token
    nuevo_access_token = create_access_token(identity=usuario_actual)

    response = make_response(jsonify({"msg":"Token refrescado"}))
    set_access_cookies(response, nuevo_access_token) 

    return response, 200

# Cerrar Sesion
@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"msg": "Logout exitoso"}))
    unset_jwt_cookies(response)
    return response, 200