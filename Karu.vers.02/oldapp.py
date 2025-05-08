from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuracion base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mi_base_datos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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

# creamos nuestra db si no existe
with app.app_context():
    db.create_all()

# una vez abierta la web
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
    ingrediente = Ingredientes.query.filter_by(id=id).first() #en todos los datos, filtramos por id
    db.session.delete(ingrediente) #eliminamos
    db.session.commit() #guardamos
    return redirect("/")

@app.route("/consumir-ingrediente/<int:id>", methods=["POST"])
def consumir_ingrediente(id):
    ingrediente = Ingredientes.query.filter_by(id=id).first()
    ingrediente.cantidad = ingrediente.cantidad - 1
    if ingrediente.cantidad == 0:
        db.session.delete(ingrediente) 
    if ingrediente.cantidad > 0:
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


if __name__ == "__main__":
    app.run(debug=True)