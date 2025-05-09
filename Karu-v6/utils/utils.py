import json
from difflib import SequenceMatcher
import requests
from models.models import Recetas, Ingredientes

API_MAGIC = 'https://magicloops.dev/api/loop/9f5a34dd-9c09-415e-913c-d3aa7022648f/run'

def obtener_nombres_recetas():
    return [r.nombre_receta.strip().lower() for r in Recetas.query.all()]

def obtener_nombres_ingredientes():
    return [i.ingrediente for i in Ingredientes.query.all()]

def armar_prompt(ingredientes, recetas_previas):
    return (
        "Crea una receta de cocina exclusivamente basada en platos convencionales, simples y caseros. "
        "Debe estar pensada para una API backend, sin explicaciones extra, y usando los ingredientes disponibles. "
        "Usa el siguiente formato JSON exacto:\n"
        "{\n"
        '  "nombre_receta": "nombre corto y claro del plato tradicional",\n'
        '  "ingredientes": {\n'
        '    "ingrediente1": "cantidad en gramos, mililitros o unidades",\n'
        '    "ingrediente2": "..."\n'
        '  },\n'
        '  "pasos": {\n'
        '    "1": "Primer paso explicado de forma clara y directa",\n'
        '    "2": "Segundo paso"\n'
        '  },\n'
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

def receta_similar(nombre, recetas_previas):
    return any(SequenceMatcher(None, nombre.lower(), r).ratio() > 0.85 for r in recetas_previas)

def llamar_api(prompt):
    payload = {"prompt": prompt}
    return requests.post(API_MAGIC, json=payload)
