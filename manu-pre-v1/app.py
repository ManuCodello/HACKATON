from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Alimento
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alimentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Cargar recetas desde archivo
with open('recetas.json', 'r') as f:
    RECETAS = json.load(f)

with app.app_context():
    db.create_all()

@app.route('/', methods =['GET', 'POST'])
def home():
    ingredientes = Alimento.query.all()
    return render_template('index.html', ingredientes=ingredientes)




@app.route('/guardar_alimentos', methods=['POST'])
def guardar_alimentos():
    datos = request.get_json()
    alimentos_guardados = []
    for fila in datos:
        alimento = Alimento(
            nombre=fila['ingrediente'].strip().lower(),
            cantidad=fila['cantidad'],
            vencimiento=fila['vencimiento'],
            tipo=fila['tipo'],
        )
        db.session.add(alimento)
        alimentos_guardados.append({
            "nombre": alimento.nombre,
            "vencimiento": alimento.vencimiento
        })

    db.session.commit()

    recetas = recomendar_con_gpt(alimentos_guardados, RECETAS)
    alertas = detectar_alertas_vencimiento(alimentos_guardados)
    return jsonify({
        "mensaje": "Alimentos guardados",
        "recetas": recetas,
        "alertas": alertas
    })

def detectar_alertas_vencimiento(alimentos):
    hoy = datetime.now().date()
    alertas = []
    for a in alimentos:
        try:
            venc = datetime.strptime(a['vencimiento'], "%Y-%m-%d").date()
            if (venc - hoy).days <= 3:
                alertas.append({
                    "nombre": a['nombre'],
                    "vencimiento": a['vencimiento']
                })
        except ValueError:
            continue
    return alertas

def recomendar_con_gpt(alimentos, recetas):
    nombres = [a['nombre'] for a in alimentos]
    alimentos_txt = ', '.join(nombres)

    recetas_txt = '\n'.join([
        f"{r['nombre']}: ingredientes: {r['ingredientes']}. pasos: {r['instrucciones']}"
        for r in recetas
    ])

    prompt = (
        f"Tengo los siguientes alimentos: {alimentos_txt}.\n"
        f"Quiero que actúes como un recomendador. Tengo esta base de recetas:\n{recetas_txt}\n\n"
        f"Recomendame 3 recetas que mejor se adapten a los ingredientes que tengo. "
        f"Respondé en JSON como lista, donde cada objeto tenga: nombre, ingredientes, pasos."
    )
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos un asistente de cocina."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        texto = respuesta.choices[0].message['content']
        try:
            recetas_sugeridas = json.loads(texto)
        except json.JSONDecodeError:
            recetas_sugeridas = texto  # Enviar texto plano si no es JSON
        return recetas_sugeridas
    except Exception as e:
        return f"Error al generar recetas: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)



