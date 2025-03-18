import bcrypt
from database.db import db

class Usuario(db.Model):
    __tablename__ = "usuarios" #Nombre de la tabla

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    creado_en = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return 'f<Usuario {self.nombre}>'
    
    def set_password(self, password):
        """Encripta la contraseña antes de guardarla."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password):
        """Verifica la contraseña encriptada."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))