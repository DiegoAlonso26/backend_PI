from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:26112004@localhost:3306/corvi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla Repuestos
class Repuestos(db.Model):
    id_repuestos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponibilidad = db.Column(db.String(50), nullable=False)
    voltaje = db.Column(db.Numeric(10, 2), nullable=False)
    imagen = db.Column(db.String(200), nullable=True)  # Nuevo campo imagen

# Crear la base de datos
with app.app_context():
    db.create_all()

# Ruta para la página de inicio
@app.route('/')
def home():
    return "Bienvenido a la API de Repuestos"

# Crear (POST)
@app.route('/repuestos', methods=['POST'])
def add_repuesto():
    data = request.get_json()
    nuevo_repuesto = Repuestos(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        precio=data['precio'],
        disponibilidad=data['disponibilidad'],
        voltaje=data['voltaje'],
        imagen=data.get('imagen')  # Nuevo campo imagen
    )
    db.session.add(nuevo_repuesto)
    db.session.commit()
    return jsonify({'message': 'Repuesto agregado con éxito'}), 201

# Leer todos los repuestos (GET)
@app.route('/repuestos', methods=['GET'])
def get_repuestos():
    repuestos = Repuestos.query.all()
    output = []
    for repuesto in repuestos:
        repuesto_data = {
            'id_repuestos': repuesto.id_repuestos,
            'nombre': repuesto.nombre,
            'descripcion': repuesto.descripcion,
            'precio': repuesto.precio,
            'disponibilidad': repuesto.disponibilidad,
            'voltaje': repuesto.voltaje,
            'imagen': repuesto.imagen  # Incluir imagen
        }
        output.append(repuesto_data)
    return jsonify(output)

# Leer un repuesto por ID (GET)
@app.route('/repuestos/<int:id>', methods=['GET'])
def get_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    return jsonify({
        'id_repuestos': repuesto.id_repuestos,
        'nombre': repuesto.nombre,
        'descripcion': repuesto.descripcion,
        'precio': repuesto.precio,
        'disponibilidad': repuesto.disponibilidad,
        'voltaje': repuesto.voltaje,
        'imagen': repuesto.imagen  # Incluir imagen
    })

# Actualizar (PUT)
@app.route('/repuestos/<int:id>', methods=['PUT'])
def update_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    data = request.get_json()
    
    repuesto.nombre = data.get('nombre', repuesto.nombre)
    repuesto.descripcion = data.get('descripcion', repuesto.descripcion)
    repuesto.precio = data.get('precio', repuesto.precio)
    repuesto.disponibilidad = data.get('disponibilidad', repuesto.disponibilidad)
    repuesto.voltaje = data.get('voltaje', repuesto.voltaje)
    repuesto.imagen = data.get('imagen', repuesto.imagen)  # Actualizar imagen
    
    db.session.commit()
    return jsonify({'message': 'Repuesto actualizado con éxito'})

# Eliminar (DELETE)
@app.route('/repuestos/<int:id>', methods=['DELETE'])
def delete_repuesto(id):
    repuesto = Repuestos.query.get_or_404(id)
    db.session.delete(repuesto)
    db.session.commit()
    return jsonify({'message': 'Repuesto eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
