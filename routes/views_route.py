from flask_jwt_extended import jwt_required
from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route("/")
def login():
    "Ruta predeterminada que muestra el login"
    return render_template('index.html')

@views_bp.route("/register")
def register():
    return render_template('register.html')

@views_bp.route('/presupuestos')
@jwt_required()
def presupuestos():
    return render_template('presupuestos.html')

@views_bp.route('/perfil')
@jwt_required()
def perfil():
    return render_template('perfil.html')

@views_bp.route('/crear_presupuesto')
@jwt_required()
def crear_presupuesto():
    return render_template('crear_presupuesto.html')

