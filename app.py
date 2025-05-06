from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configuracion base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tareas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# modelo de datos en SQL
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingrediente = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    vencimiento = db.Column(db.String(20), nullable=True)
    consumida = db.Column(db.Boolean, default=False)

# creamos nuestra db si no existe
with app.app_context():
    db.create_all()

# una vez abierta la web
@app.route("/", methods=["GET", "POST"])
def home():
    ingredientes = Ingrediente.query.all() #guardamos en tareas nuestra base de datos
    return render_template("index.html", ingredientes=ingredientes) #tareas de html == tareas de python

@app.route("/agregar-ingrediente", methods=["POST"])
def agregar_ingrediente():

    nuevo_ingrediente = Ingrediente(
        ingrediente = request.form["ingrediente"],
        cantidad = request.form["cantidad"],
        vencimiento = request.form["vencimiento"],
    )
    db.session.add(nuevo_ingrediente) #añade a la db
    db.session.commit() #guarda la db
    return redirect("/")

@app.route("/eliminar-ingrediente/<int:id>", methods=["POST"])
def eliminar_ingrediente(id):
    ingrediente = Ingrediente.query.filter_by(id=id).first() #en todos los datos, filtramos por id
    db.session.delete(ingrediente) #eliminamos
    db.session.commit() #guardamos
    return redirect("/")

@app.route("/cambiar-estado/<int:id>", methods=["POST"])
def cambiar_estado(id):
    ingrediente = Ingrediente.query.filter_by(id=id).first()
    ingrediente.consumida = not ingrediente.consumida
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)