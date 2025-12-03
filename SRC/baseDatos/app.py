from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Administrador, Evento, Entrada  # Importamos modelos necesarios

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

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    # BocetoHome
    return render_template('index.html')

@app.route('/quienes-somos')
def quienes_somos():
    # BocetoUS (Misión, Historia, Equipo)
    return render_template('quienes_somos.html')

@app.route('/contacto')
def contacto():
    # BocetoContacto
    return render_template('contacto.html')

# --- RUTAS DE EVENTOS ---

@app.route('/eventos')
def eventos():
    # (listado)Eventos
    lista_eventos = Evento.query.all()
    rifas = [
        {
            "id": 1,
            "titulo": "Rifa Cesta Solidaria",
            "premio": "Cesta con productos locales y artesanales.",
            "fecha_sorteo": "20/12/2025",
            "descripcion": "Incluye productos típicos del municipio.",
            "imagen": "img/rifa-cesta.jpg"
        }
    ]
    return render_template('eventos.html', eventos=lista_eventos, rifas=rifas)

@app.route('/evento/<int:id>')
def ver_evento(id):
    # verEvento
    evento = Evento.query.get_or_404(id)
    return render_template('ver_evento.html', evento=evento)

def get_rifas():
    return {
        1: {
            "id": 1,
            "titulo": "Rifa Cesta Solidaria",
            "premio": "Cesta con productos locales y artesanales.",
            "fecha_sorteo": "20/12/2025",
            "descripcion": "Incluye productos típicos del municipio.",
            "imagen": "img/rifa-cesta.jpg"
        }
    }

@app.route('/rifa/<int:id>')
def ver_rifa(id):
    rifas = get_rifas()
    rifa = rifas.get(id)
    if not rifa:
        abort(404)
    return render_template('rifa.html', rifa=rifa)

@app.route('/rifa/<int:id>/participar', methods=['GET', 'POST'])
@login_required
def participar_rifa(id):
    rifas = get_rifas()
    rifa = rifas.get(id)

    if not rifa:
        abort(404)

    if request.method == 'POST':
        # cantidad de boletos para la rifa (como cantidad_entradas)
        cantidad_boletos = int(request.form.get('cantidad', 1))

        # Aquí podrías guardar en BD como haces con Entrada
        # Por ahora solo simulamos la participación
        flash(f'¡Has participado con {cantidad_boletos} boletos en la rifa "{rifa["titulo"]}"!')
        return redirect(url_for('dashboard'))

    # GET → mostramos página similar a pago_entrada
    return render_template('participar_rifa.html', rifa=rifa)

@app.route('/evento/comprar/<int:id_evento>', methods=['GET', 'POST'])
@login_required
def pago_entrada(id_evento):
    # pagoEntrada
    evento = Evento.query.get_or_404(id_evento)
    if request.method == 'POST':
        cantidad_entradas = int(request.form.get('cantidad', 1))
        # Aquí iría la lógica de pasarela de pago real
        # Por ahora simulamos la creación de entradas
        for _ in range(cantidad_entradas):
            nueva_entrada = Entrada(
                precio=20.0, # Precio ejemplo
                id_evento=evento.id,
                id_comprador=current_user.id,
                codigo_qr="QR_GENERADO_SIMULADO"
            )
            db.session.add(nueva_entrada)
        db.session.commit()
        flash('¡Entradas compradas con éxito!')
        return redirect(url_for('dashboard'))
        
    return render_template('pago_entrada.html', evento=evento)

# --- RUTAS DE SOCIOS / DONACIONES ---

@app.route('/hazte-socio', methods=['GET', 'POST'])
def hazte_socio():
    # BocetoHazteSocio_Persona y Empresa
    if request.method == 'POST':
        # Lógica para procesar el formulario de socio
        flash('Gracias por tu solicitud de socio. Te contactaremos pronto.')
        return redirect(url_for('index'))
    return render_template('hazte_socio.html')

@app.route('/hazte-voluntario', methods=['GET', 'POST'])
def hazte_voluntario():
    # BocetoHazteSocio_Persona y Empresa
    if request.method == 'POST':
        # Lógica para procesar el formulario de socio
        flash('Gracias por tu solicitud de socio. Te contactaremos pronto.')
        return redirect(url_for('index'))
    return render_template('hazte_voluntario.html')

@app.route('/donar')
def donar():
    # Reutilizamos la vista de socios o una simplificada
    return redirect(url_for('hazte_socio'))

# --- RUTAS DE AUTENTICACIÓN (Tus rutas originales mejoradas) ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        # En el boceto registro hay nombre? Asumiremos que se usa parte del email o se añade el campo
        nombre = request.form.get('nombre', email.split('@')[0]) 
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')
        
        if password != password_repeat:
            flash('Las contraseñas no coinciden')
            return render_template('registro.html')

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
        
        # --- DATOS DE PRUEBA (SOLO PARA VER QUE FUNCIONA) ---
        if not Evento.query.first():
            evento_demo = Evento(
                nombre_evento="Gala Benéfica James Bond",
                localizacion="Rotary Club Marbella",
                fecha=None, # Pon un datetime real aquí
                informacion="Una velada inolvidable..."
            )
            db.session.add(evento_demo)
            db.session.commit()
            
    app.run(debug=True)