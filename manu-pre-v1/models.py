from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100))
    vencimiento = db.Column(db.String(20))  # en formato AAAA-MM-DD


