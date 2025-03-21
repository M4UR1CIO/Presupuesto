from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config.config import Config
from database.db import db
from routes.auth_route import auth_bp
from routes.presupuesto_route import presupuesto_bp
from routes.gastos_routes import gasto_bp
from routes.views_route import views_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar SQLAlchemy con la app
db.init_app(app)

# Colocar JWT
jwt = (JWTManager(app))

# Ruta para mensaje personalizado al no encontrar la ruta buscada
@app.errorhandler(404)
def pagina_no_encontrada(error): # Varible de error
    return render_template('404.html', error=error) # Ruta para el html de error

# Rutas
app.register_blueprint(views_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(presupuesto_bp)
app.register_blueprint(gasto_bp)

if __name__ == "__main__":
    app.run(debug=True)
