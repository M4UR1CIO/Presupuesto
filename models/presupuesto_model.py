from database.db import db
from sqlalchemy import func

class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_presupuesto = db.Column(db.Integer, nullable=False)  # Nuevo campo
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    fecha_creacion = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('presupuestos', lazy=True))

    def __repr__(self):
        return f'<Presupuesto {self.nombre}>'

    @staticmethod
    def obtener_siguiente_numero(usuario_id):
        ultimo = db.session.query(func.max(Presupuesto.numero_presupuesto)).filter_by(usuario_id=usuario_id).scalar()
        return (ultimo or 0) + 1