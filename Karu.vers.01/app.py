from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from difflib import SequenceMatcher

app = Flask(__name__)

# Configuración base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mi_base_datos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELOS
class Ingredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingrediente = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    guardado = db.Column(db.String(20), nullable=False)
    vencimiento = db.Column(db.String(20), nullable=True)

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

with app.app_context():
    db.create_all()

# HOME
@app.route("/", methods=["GET", "POST"])
def home():
    ingredientes = Ingredientes.query.all() 
    recetas = Recetas.query.all()
    return render_template("index.html", recetas=recetas, ingredientes=ingredientes) 

@app.route("/agregar-ingredientes", methods=["POST"])
def agregar_ingrediente():
    data = request.get_json()
    for item in data:
        nombre = item["ingrediente"].strip().lower()
        cantidad = int(item["cantidad"])
        unidad = item["unidad"]
        tipo = item["tipo"]
        guardado = item["guardado"]
        vencimiento = item["vencimiento"]

        existente = Ingredientes.query.filter_by(ingrediente=nombre).first()

        if existente:
            existente.cantidad += cantidad
        else:
            nuevo = Ingredientes(
                ingrediente=nombre,
                cantidad=cantidad,
                unidad=unidad,
                tipo=tipo,
                guardado=guardado,
                vencimiento=vencimiento
            )
            db.session.add(nuevo)

    db.session.commit()
    return redirect("/")

@app.route("/eliminar-ingrediente/<int:id>", methods=["POST"])
def eliminar_ingrediente(id):
    ingrediente = Ingredientes.query.filter_by(id=id).first()
    db.session.delete(ingrediente)
    db.session.commit()
    return redirect("/")

@app.route("/consumir-ingrediente/<int:id>", methods=["POST"])
def consumir_ingrediente(id):
    ingrediente = Ingredientes.query.filter_by(id=id).first()
    if ingrediente.cantidad == 1:
        db.session.delete(ingrediente)
    elif ingrediente.cantidad > 1:
        ingrediente.cantidad -= 1
    db.session.commit()
    return redirect("/")

@app.route("/receta/<int:id>")
def obtener_receta(id):
    receta = Recetas.query.get(id)
    if receta:
        return jsonify({
            "id": receta.id,
            "nombre_receta": receta.nombre_receta,
            "descripcion": receta.descripcion,
            "ingredientes": receta.ingredientes,
            "pasos": receta.pasos,
            "tiempo": receta.tiempo,
            "categoria": receta.categoria,
            "dieta": receta.dieta,
            "porciones": receta.porciones,
            "calorias": receta.calorias,
            "proteina": receta.proteina,
            "grasa": receta.grasa,
            "carbohidratos": receta.carbohidratos
        })
    else:
        return jsonify({"error": "Receta no encontrada"}), 404

@app.route("/todas-las-recetas")
def todas_las_recetas():
    recetas = Recetas.query.all()
    recetas_lista = [
        {
            "id": receta.id,
            "nombre_receta": receta.nombre_receta,
            "descripcion": receta.descripcion,
            "ingredientes": receta.ingredientes,
            "pasos": receta.pasos,
            "tiempo": receta.tiempo,
            "categoria": receta.categoria,
            "dieta": receta.dieta,
            "porciones": receta.porciones,
            "calorias": receta.calorias,
            "proteina": receta.proteina,
            "grasa": receta.grasa,
            "carbohidratos": receta.carbohidratos
        }
        for receta in recetas
    ]
    return jsonify(recetas_lista)

@app.route("/crear-receta", methods=["POST"])
def crear_receta():
    nueva_receta = request.get_json()
    receta = Recetas(
        nombre_receta=nueva_receta["nombre_receta"],
        descripcion=nueva_receta["descripcion"],
        ingredientes=nueva_receta["ingredientes"],
        pasos=nueva_receta["pasos"],
        tiempo=nueva_receta["tiempo"],
        categoria=nueva_receta["categoria"],
        dieta=nueva_receta["dieta"],
        porciones=nueva_receta["porciones"],
        calorias=nueva_receta["calorias"],
        proteina=nueva_receta["proteina"],
        grasa=nueva_receta["grasa"],
        carbohidratos=nueva_receta["carbohidratos"]
    )
    db.session.add(receta)
    db.session.commit()
    return jsonify({"message": "Receta creada exitosamente", "id": receta.id})

# ------------------------------------------------
# 🔁 RUTA DE INTEGRACIÓN CON MAGIC LOOPS
# ------------------------------------------------

API_MAGIC = 'https://magicloops.dev/api/loop/9f5a34dd-9c09-415e-913c-d3aa7022648f/run'

def obtener_nombres_recetas():
    return [r.nombre_receta.strip().lower() for r in Recetas.query.all()]

def obtener_nombres_ingredientes():
    return [i.ingrediente for i in Ingredientes.query.all()]

def armar_prompt(ingredientes, recetas_previas):
    prompt = (
        "Crea una receta de cocina exclusivamente basada en platos convencionales, simples y caseros. "
        "Debe estar pensada para una API backend, sin explicaciones extra, y usando los ingredientes disponibles. "
        "Usa el siguiente formato JSON exacto:\n"
        "{\n"
        '  "nombre_receta": "nombre corto y claro del plato tradicional",\n'
        '  "ingredientes": {\n'
        '    "ingrediente1": "cantidad en gramos, mililitros o unidades",\n'
        '    "ingrediente2": "..."\n'
        "  },\n"
        '  "pasos": {\n'
        '    "1": "Primer paso explicado de forma clara y directa",\n'
        '    "2": "Segundo paso"\n'
        "  },\n"
        '  "descripcion": "Breve explicación del plato y su uso común en hogares o su contexto cultural",\n'
        '  "tiempo": "Duración total estimada (ej: 45 minutos)",\n'
        '  "categoria": "Almuerzo, Cena, Merienda, Desayuno, etc.",\n'
        '  "dieta": "especificar si es sin gluten, vegetariano, etc.",\n'
        '  "porciones": 4,\n'
        '  "calorias": 400,\n'
        '  "proteina": "10g",\n'
        '  "grasa": "15g",\n'
        '  "carbohidratos": "50g"\n'
        "}\n\n"
        f"Tengo estos ingredientes disponibles: {', '.join(ingredientes)}.\n"
        f"Ya se generaron estas recetas: {', '.join(recetas_previas)}.\n"
        "Generá una receta nueva, que no repita ninguna de las anteriores y que use preferentemente los ingredientes disponibles. "
        "Devuelve únicamente formato JSON válido."
    )
    return prompt

def receta_similar(nombre, recetas_previas):
    return any(SequenceMatcher(None, nombre.lower(), r).ratio() > 0.85 for r in recetas_previas)

@app.route("/generar-receta-inteligente", methods=["POST"])
def generar_receta_ia():
    ingredientes = obtener_nombres_ingredientes()
    recetas_previas = obtener_nombres_recetas()

    for _ in range(5):  # máximo 5 intentos
        prompt = armar_prompt(ingredientes, recetas_previas)
        payload = {"prompt": prompt}
        response = requests.post(API_MAGIC, json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Error al conectar con Magic Loops"}), 500

        try:
            receta_data = json.loads(response.text.strip())
        except json.JSONDecodeError:
            return jsonify({"error": "Respuesta no es JSON válido"}), 500

        nombre_generado = receta_data.get("nombre_receta", "").strip().lower()

        if receta_similar(nombre_generado, recetas_previas):
            continue  # intenta generar una nueva

        nueva = Recetas(
            nombre_receta=receta_data["nombre_receta"],
            descripcion=receta_data["descripcion"],
            ingredientes="; ".join([f"{k}: {v}" for k, v in receta_data["ingredientes"].items()]),
            pasos=" | ".join([f"{k}. {v}" for k, v in receta_data["pasos"].items()]),
            tiempo=receta_data["tiempo"],
            categoria=receta_data["categoria"],
            dieta=receta_data["dieta"],
            porciones=receta_data["porciones"],
            calorias=receta_data["calorias"],
            proteina=receta_data["proteina"],
            grasa=receta_data["grasa"],
            carbohidratos=receta_data["carbohidratos"]
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({"mensaje": "Receta generada correctamente", "receta": receta_data})

    return jsonify({"error": "No se pudo generar una receta nueva tras varios intentos"}), 400

# ----------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)