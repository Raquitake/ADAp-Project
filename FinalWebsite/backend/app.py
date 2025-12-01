from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Administrador, Evento, Rifa
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True) # Enable CORS for all routes

app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'
# Ensure we use the absolute path or correct relative path to the database in the instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- RUTAS TRADICIONALES (Legacy/Fallback) ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        tipo_usuario = request.form.get('tipo')

        usuario_existente = Usuario.query.filter_by(correo_electronico=email).first()
        if usuario_existente:
            flash('El correo ya está registrado.')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuario(
            nombre_usuario=nombre,
            correo_electronico=email,
            contrasena_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            es_socio=False
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        if tipo_usuario == 'admin':
            nuevo_admin = Administrador(id_usuario=nuevo_usuario.id)
            db.session.add(nuevo_admin)
            db.session.commit()
        
        login_user(nuevo_usuario)
        return redirect(url_for('dashboard'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(correo_electronico=email).first()

        if usuario and check_password_hash(usuario.contrasena_hash, password):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos.')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- API ENDPOINTS ---

@app.route('/api/eventos', methods=['GET'])
def get_eventos():
    eventos = Evento.query.all()
    return jsonify([evento.to_dict() for evento in eventos])

@app.route('/api/rifas', methods=['GET'])
def get_rifas():
    rifas = Rifa.query.all()
    return jsonify([rifa.to_dict() for rifa in rifas])

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    usuario = Usuario.query.filter_by(correo_electronico=email).first()

    if usuario and check_password_hash(usuario.contrasena_hash, password):
        login_user(usuario)
        return jsonify({'message': 'Login successful', 'user': {'id': usuario.id, 'nombre': usuario.nombre_usuario, 'email': usuario.correo_electronico, 'es_admin': usuario.es_admin}})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    password = data.get('password')
    # tipo_usuario = data.get('tipo') # Optional for now

    usuario_existente = Usuario.query.filter_by(correo_electronico=email).first()
    if usuario_existente:
        return jsonify({'error': 'Email already registered'}), 400

    nuevo_usuario = Usuario(
        nombre_usuario=nombre,
        correo_electronico=email,
        contrasena_hash=generate_password_hash(password, method='pbkdf2:sha256'),
        es_socio=False
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    login_user(nuevo_usuario)
    return jsonify({'message': 'Registration successful', 'user': {'id': nuevo_usuario.id, 'nombre': nuevo_usuario.nombre_usuario, 'email': nuevo_usuario.correo_electronico}})

@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': {'id': current_user.id, 'nombre': current_user.nombre_usuario, 'email': current_user.correo_electronico, 'es_admin': current_user.es_admin}})
    return jsonify({'authenticated': False})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)