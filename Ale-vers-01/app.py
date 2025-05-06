from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuracion base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ingredientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# modelo de datos en SQL
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingrediente = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    vencimiento = db.Column(db.String(20), nullable=True)
    

# creamos nuestra db si no existe
with app.app_context():
    db.create_all()

# una vez abierta la web
@app.route("/", methods=["GET", "POST"])
def home():
    ingredientes = Ingrediente.query.all() #guardamos en tareas nuestra base de datos
    return render_template("index.html", ingredientes=ingredientes) #tareas de html == tareas de python

@app.route("/agregar-ingredientes", methods=["POST"])
def agregar_ingrediente():
    data = request.get_json()

    for item in data:
        nombre = item["ingrediente"].strip().lower()
        cantidad = int(item["cantidad"])
        tipo = item["tipo"]
        vencimiento = item["vencimiento"]

        existente = Ingrediente.query.filter_by(ingrediente=nombre).first()

        if existente:
            existente.cantidad += cantidad
        else:
            nuevo = Ingrediente(
                ingrediente=nombre,
                cantidad=cantidad,
                tipo=tipo,
                vencimiento=vencimiento
            )
            db.session.add(nuevo)

    db.session.commit()
    return redirect("/")

@app.route("/eliminar-ingrediente/<int:id>", methods=["POST"])
def eliminar_ingrediente(id):
    ingrediente = Ingrediente.query.filter_by(id=id).first() #en todos los datos, filtramos por id
    db.session.delete(ingrediente) #eliminamos
    db.session.commit() #guardamos
    return redirect("/")

@app.route("/consumir-ingrediente/<int:id>", methods=["POST"])
def consumir_ingrediente(id):
    ingrediente = Ingrediente.query.filter_by(id=id).first()
    ingrediente.cantidad = ingrediente.cantidad - 1
    if ingrediente.cantidad == 0:
        db.session.delete(ingrediente) 
    if ingrediente.cantidad > 0:
        ingrediente.cantidad -= 1
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)