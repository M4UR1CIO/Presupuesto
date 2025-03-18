from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config.config import Config
from database.db import db
from routes.auth_route import auth_bp
from routes.presupuesto_route import presupuesto_bp
from routes.gastos_routes import gasto_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar SQLAlchemy con la app
db.init_app(app)

# Colocar JWT
jwt = (JWTManager(app))

@app.route('/')
def login():
    return render_template('index.html')

# Rutas
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(presupuesto_bp)
app.register_blueprint(gasto_bp)

if __name__ == "__main__":
    app.run(debug=True)
