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

@views_bp.route("/sidebar")
@jwt_required()
def dashboard():
    return render_template('sidebar.html')

@views_bp.route('/presupuestos')
def presupuestos():
    return render_template('presupuestos.html')