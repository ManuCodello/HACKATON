# Importa Flask, db (de models) y routes (de routes)
from flask import Flask
from models.models import db
from routes.routes import routes

# Crea la aplicación Flask
app = Flask(__name__)

# Configura la URI de la base de datos y desactiva el seguimiento de modificaciones de SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mi_base_datos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa la base de datos con la aplicación
db.init_app(app)

# Registra las rutas desde el blueprint 'routes'
app.register_blueprint(routes)

# Crea las tablas en la base de datos dentro del contexto de la aplicación
with app.app_context():
    db.create_all()

# Ejecuta la aplicación en modo debug si el archivo es ejecutado directamente
if __name__ == "__main__":
    app.run(debug=True)
