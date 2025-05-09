# Importa SQLAlchemy para manejar la base de datos en Flask
from flask_sqlalchemy import SQLAlchemy

# Se instancia el objeto db para interactuar con la base de datos
db = SQLAlchemy()

# Modelo de base de datos para los ingredientes
class Ingredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    ingrediente = db.Column(db.String(100), nullable=False)  
    cantidad = db.Column(db.Integer, nullable=False)  
    unidad = db.Column(db.String(20), nullable=False)  
    tipo = db.Column(db.String(20), nullable=False)  
    guardado = db.Column(db.String(20), nullable=False)  
    vencimiento = db.Column(db.String(20), nullable=True) 

# Modelo de base de datos para las recetas
class Recetas(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    nombre_receta = db.Column(db.String(100), nullable=False)  
    descripcion = db.Column(db.String(255), nullable=False)  
    ingredientes = db.Column(db.String(255), nullable=True) 
    pasos = db.Column(db.String(255), nullable=False)  
    tiempo = db.Column(db.String(50), nullable=False)  
    categoria = db.Column(db.String(50), nullable=False)  
    dieta = db.Column(db.String(100), nullable=True)  
    porciones = db.Column(db.Integer, nullable=False)  
    calorias = db.Column(db.Integer, nullable=False) 
    proteina = db.Column(db.String(20), nullable=False)  
    grasa = db.Column(db.String(20), nullable=False)  
    carbohidratos = db.Column(db.String(20), nullable=False)  
