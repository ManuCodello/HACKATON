# Se importan las librerías necesarias para el funcionamiento de la aplicación Flask
from flask import Blueprint, render_template, request, redirect, jsonify
from models.models import db, Ingredientes, Recetas  # Importación de modelos de base de datos
from utils.utils import *  # Funciones utilitarias adicionales
import json

# Se crea un Blueprint llamado 'routes' para organizar las rutas
routes = Blueprint('routes', __name__)

# Ruta principal que muestra todos los ingredientes y recetas en la página de inicio
@routes.route("/", methods=["GET"])
def home():
    ingredientes = Ingredientes.query.all()  # Recupera todos los ingredientes desde la base de datos
    recetas = Recetas.query.all()  # Recupera todas las recetas desde la base de datos
    return render_template("index.html", recetas=recetas, ingredientes=ingredientes)  # Renderiza la vista 'index.html'

# Ruta para agregar nuevos ingredientes a la base de datos
@routes.route("/agregar-ingredientes", methods=["POST"])
def agregar_ingrediente():
    data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud
    for item in data:
        # Procesa los datos del ingrediente recibido
        nombre = item["ingrediente"].strip().lower()
        cantidad = int(item["cantidad"])
        unidad = item["unidad"]
        tipo = item["tipo"]
        guardado = item["guardado"]
        vencimiento = item["vencimiento"]

        # Verifica si el ingrediente ya existe en la base de datos
        existente = Ingredientes.query.filter_by(ingrediente=nombre).first()

        if existente:
            # Si existe, se aumenta la cantidad del ingrediente
            existente.cantidad += cantidad
        else:
            # Si no existe, se crea un nuevo registro de ingrediente
            nuevo = Ingredientes(
                ingrediente=nombre,
                cantidad=cantidad,
                unidad=unidad,
                tipo=tipo,
                guardado=guardado,
                vencimiento=vencimiento
            )
            db.session.add(nuevo)  # Agrega el nuevo ingrediente a la sesión de la base de datos

    db.session.commit()  # Guarda los cambios en la base de datos
    return redirect("/")  # Redirige a la página principal

# Ruta para eliminar un ingrediente de la base de datos
@routes.route("/eliminar-ingrediente/<int:id>", methods=["POST"])
def eliminar_ingrediente(id):
    ingrediente = Ingredientes.query.filter_by(id=id).first()  # Busca el ingrediente por su id
    db.session.delete(ingrediente)  # Elimina el ingrediente de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios
    return redirect("/")  # Redirige a la página principal

# Ruta para consumir un ingrediente, decrementando su cantidad
@routes.route("/consumir-ingrediente/<int:id>", methods=["POST"])
def consumir_ingrediente(id):
    ingrediente = Ingredientes.query.filter_by(id=id).first()  # Busca el ingrediente por su id
    if ingrediente.cantidad == 1:
        db.session.delete(ingrediente)  # Si la cantidad es 1, elimina el ingrediente
    elif ingrediente.cantidad > 1:
        ingrediente.cantidad -= 1  # Si la cantidad es mayor que 1, decrementa la cantidad
    db.session.commit()  # Guarda los cambios
    return redirect("/")  # Redirige a la página principal

# Ruta para obtener una receta específica por su id en formato JSON
@routes.route("/receta/<int:id>")
def obtener_receta(id):
    receta = Recetas.query.get(id)  # Busca la receta por su id
    if receta:
        # Si la receta existe, retorna un JSON con los detalles de la receta
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
        # Si la receta no existe, retorna un error 404
        return jsonify({"error": "Receta no encontrada"}), 404

# Ruta para obtener todas las recetas en formato JSON
@routes.route("/todas-las-recetas")
def todas_las_recetas():
    recetas = Recetas.query.all()  # Recupera todas las recetas de la base de datos
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
        } for receta in recetas  # Convierte todas las recetas en una lista de diccionarios
    ]
    return jsonify(recetas_lista)  # Devuelve la lista de recetas en formato JSON

# Ruta para crear una nueva receta a partir de datos JSON
@routes.route("/crear-receta", methods=["POST"])
def crear_receta():
    nueva_receta = request.get_json()  # Obtiene los datos de la nueva receta en formato JSON
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
    db.session.add(receta)  # Agrega la receta a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios
    return jsonify({"message": "Receta creada exitosamente", "id": receta.id})  # Retorna un mensaje de éxito

# Ruta para generar una receta inteligente usando una API externa
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


@routes.route("/generar-receta-inteligente", methods=["POST"])
def generar_receta_ia():
    ingredientes = obtener_nombres_ingredientes()
    recetas_previas = obtener_nombres_recetas()

    for _ in range(5):
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
            continue

        return jsonify({"receta": receta_data})

    return jsonify({"error": "No se pudo generar una receta nueva tras varios intentos"}), 400

@routes.route("/guardar-receta", methods=["POST"])
def guardar_receta():
    receta_data = request.json

    try:
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

        return jsonify({"mensaje": "Receta guardada exitosamente"})
    except Exception as e:
        return jsonify({"error": f"No se pudo guardar la receta: {str(e)}"}), 500

