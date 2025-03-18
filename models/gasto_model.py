from database.db import db

class Gasto(db.Model):
    __tablename__ = 'gastos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable=False)
    monto = db.Column(db.Float, nullable=False, default=0.0)
    fecha = db.Column(db.Date, nullable=False)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'), nullable=False)

    presupuesto = db.relationship('Presupuesto', backref=db.backref('gastos', lazy=True))

    def __repr__(self):
        return f'<Gasto {self.descripcion}>'