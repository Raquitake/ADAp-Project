from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Administrador 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- RUTAS ---
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)