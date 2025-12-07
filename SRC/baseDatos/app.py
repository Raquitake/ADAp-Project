import os
import re
import qrcode
import uuid

from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from models import db, Usuario, Administrador, Evento, Entrada, Rifa, Boleto

# [IMPORT PATTERNS]
from patterns import AppConfig, PaymentFactory, EventoBuilder, EventTransactionFactory, RaffleTransactionFactory

def validar_dni_nie(documento):
    documento = documento.upper().strip()
    if len(documento) != 9: return False
    letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
    letra_usuario = documento[-1]
    parte_numerica = documento[:-1]
    if parte_numerica.startswith('X'): parte_numerica = '0' + parte_numerica[1:]
    elif parte_numerica.startswith('Y'): parte_numerica = '1' + parte_numerica[1:]
    elif parte_numerica.startswith('Z'): parte_numerica = '2' + parte_numerica[1:]
    if not parte_numerica.isdigit(): return False
    resto = int(parte_numerica) % 23
    return letras_validas[resto] == letra_usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# [SINGLETON CONFIG SETUP]
# Definimos las rutas en app.config para que el Singleton las lea al inicializarse
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'eventos')
app.config['RIFA_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'rifas')
app.config['QR_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'qrcodes')

# Inicializamos el Singleton
app_config = AppConfig()
app_config.init_app(app)

db.init_app(app)

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- ADMIN DECORATOR ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# --- RUTAS DE EVENTOS ---

@app.route('/eventos')
def eventos():
    lista_eventos = Evento.query.all()
    lista_rifas = Rifa.query.all()
    return render_template('eventos.html', eventos=lista_eventos, rifas=lista_rifas)

@app.route('/evento/<int:id>')
def ver_evento(id):
    evento = Evento.query.get_or_404(id)
    return render_template('ver_evento.html', evento=evento)

@app.route('/rifa/<int:id>')
def ver_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    return render_template('rifa.html', rifa=rifa)

@app.route('/rifa/<int:id>/participar', methods=['GET', 'POST'])
@login_required
def participar_rifa(id):
    rifa = Rifa.query.get_or_404(id)

    if request.method == 'POST':
        cantidad_boletos = int(request.form.get('cantidad', 1))
        metodo_pago = request.form.get('metodo_pago')

        # [FACTORY METHOD]: Payment Processing
        processor = PaymentFactory.get_processor(metodo_pago)
        if not processor:
             flash('Método de pago no válido')
             return redirect(url_for('participar_rifa', id=id))
             
        # Placeholder Amount logic
        success, msg = processor.process(10.0 * cantidad_boletos, request.form)
        if not success:
            flash(f"Error en el pago: {msg}")
            return render_template('participar_rifa.html', rifa=rifa)

        # [ABSTRACT FACTORY]: Create Database Record (Boleto) and Token (None for Rifa)
        factory = RaffleTransactionFactory()
        
        try:
             for _ in range(cantidad_boletos):
                 # No access token for rifa needed
                 db_record = factory.create_database_record(rifa.id, current_user.id, 0.0) # Precio simbolico
                 db.session.add(db_record)
                 
             db.session.commit()
             flash(f'Has comprado {cantidad_boletos} boletos para "{rifa.nombre}". {msg}')
             return redirect(url_for('dashboard'))
             
        except Exception as e:
            db.session.rollback()
            flash(f"Error procesando compra: {e}")

    return render_template('participar_rifa.html', rifa=rifa)

@app.route('/evento/comprar/<int:id_evento>', methods=['GET', 'POST'])
@login_required
def pago_entrada(id_evento):
    evento = Evento.query.get_or_404(id_evento)
    
    if request.method == 'POST':
        try:
            cantidad_entradas = int(request.form.get('cantidad', 1))
        except ValueError:
            cantidad_entradas = 1
            
        metodo_pago = request.form.get('metodo_pago')

        # [FACTORY METHOD]
        processor = PaymentFactory.get_processor(metodo_pago)
        if not processor:
             flash('Método de pago desconocido')
             return render_template('pago_entrada.html', evento=evento)
             
        success, msg = processor.process(evento.precio * cantidad_entradas, request.form)
        
        if not success:
            flash(f"❌ Pago fallido: {msg}")
            return render_template('pago_entrada.html', evento=evento)

        # [ABSTRACT FACTORY]
        # Crear Entradas (DB) y QRs (Access Token)
        factory = EventTransactionFactory()
        
        try:
            for _ in range(cantidad_entradas):
                # Crear QR
                token_path = factory.create_access_token() 
                # Crear Entrada
                entrada = factory.create_database_record(evento.id, current_user.id, evento.precio, token_path)
                db.session.add(entrada)
            
            db.session.commit()
            flash(f'✅ ¡Pago exitoso! {cantidad_entradas} entradas generadas.')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error DB: {e}")
            flash('❌ Hubo un error al generar las entradas.')
            return render_template('pago_entrada.html', evento=evento)
        
    return render_template('pago_entrada.html', evento=evento)

# --- RUTAS DE ADMINISTRACIÓN ---

@app.route('/admin/evento/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_evento():
    if request.method == 'POST':
        # [BUILDER PATTERN]
        try:
            builder = EventoBuilder()
            nuevo_evento = (builder
                .set_basic_info(
                    nombre=request.form.get('nombre'),
                    localizacion=request.form.get('localizacion'),
                    informacion=request.form.get('informacion')
                )
                .set_date(request.form.get('fecha'))
                .set_price(request.form.get('precio'))
                .set_image(request.files.get('imagen'))
                .build()
            )
            db.session.add(nuevo_evento)
            db.session.commit()
            flash('Evento creado exitosamente (Builder Pattern)')
            return redirect(url_for('eventos'))
        except Exception as e:
            print(f"Error builder: {e}")
            flash("Error creando evento")
            
    return render_template('admin/crear_evento.html')

@app.route('/admin/evento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_evento(id):
    evento = Evento.query.get_or_404(id)
    if request.method == 'POST':
        evento.nombre_evento = request.form.get('nombre')
        evento.localizacion = request.form.get('localizacion')
        evento.informacion = request.form.get('informacion')
        evento.precio = float(request.form.get('precio', 0.0))
        
        fecha_str = request.form.get('fecha')
        if fecha_str:
            try:
                evento.fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                pass
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                # Se podría usar Singleton AppConfig aquí también
                config = AppConfig()
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(config.get_upload_folder, filename))
                evento.imagen_evento = f"img/eventos/{filename}"

        db.session.commit()
        flash('Evento actualizado')
        return redirect(url_for('ver_evento', id=id))
    return render_template('admin/editar_evento.html', evento=evento)

@app.route('/admin/evento/eliminar/confirmar/<int:id>')
@login_required
@admin_required
def confirmar_eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    return render_template('admin/confirmar_eliminar_evento.html', evento=evento)

@app.route('/admin/evento/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_evento(id):
    evento = Evento.query.get_or_404(id)
    # Using Singleton for path
    if evento.imagen_evento:
        config = AppConfig()
        filename = os.path.basename(evento.imagen_evento)
        image_path = os.path.join(config.get_upload_folder, filename)
        if os.path.exists(image_path):
             try: os.remove(image_path)
             except: pass
    
    db.session.delete(evento)
    db.session.commit()
    flash('Evento eliminado')
    return redirect(url_for('eventos'))

# [PROTOTYPE] Route to test cloning
@app.route('/admin/evento/clonar/<int:id>')
@login_required
@admin_required
def clonar_evento(id):
    original = Evento.query.get_or_404(id)
    # Cloning using the Prototype method
    clon = original.clone()
    db.session.add(clon)
    db.session.commit()
    flash(f'Evento clonado: {clon.nombre_evento}')
    return redirect(url_for('eventos'))

@app.route('/admin/socios')
@login_required
@admin_required
def gestionar_socios():
    socios = Usuario.query.filter_by(es_socio=True).all()
    return render_template('admin/gestionar_socios.html', socios=socios)

@app.route('/admin/socio/<int:id>')
@login_required
@admin_required
def ver_socio_admin(id):
    socio = Usuario.query.get_or_404(id)
    entradas = Entrada.query.filter_by(id_comprador=socio.id).all()
    boletos = Boleto.query.filter_by(id_comprador=socio.id).all()
    return render_template('admin/ver_socio.html', socio=socio, entradas=entradas, boletos=boletos)

@app.route('/baja-socio', methods=['POST'])
@login_required
def baja_socio():
    if current_user.es_socio:
        current_user.es_socio = False
        db.session.commit()
        flash('Has dado de baja tu suscripción.')
    return redirect(url_for('dashboard'))

# --- GESTIÓN DE RIFAS (ADMIN) ---

@app.route('/admin/rifas')
@login_required
@admin_required
def gestionar_rifas():
    rifas = Rifa.query.all()
    return render_template('admin/gestionar_rifas.html', rifas=rifas)

@app.route('/admin/rifa/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_rifa():
    if request.method == 'POST':
        # Could use Builder here too, but restricted to Evento per explicit request instructions
        nombre = request.form.get('nombre')
        premio = request.form.get('premio')
        informacion = request.form.get('informacion')
        fecha_str = request.form.get('fecha')
        
        fecha_fin = None
        if fecha_str:
            try: fecha_fin = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            except: pass

        imagen_path = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                config = AppConfig()
                filename = f"rifa_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(config.get_rifa_upload_folder, filename))
                imagen_path = f"img/rifas/{filename}"

        nueva_rifa = Rifa(
            nombre=nombre,
            premio=premio,
            informacion=informacion,
            fecha_fin=fecha_fin,
            imagen=imagen_path
        )
        db.session.add(nueva_rifa)
        db.session.commit()
        flash('Rifa creada')
        return redirect(url_for('gestionar_rifas'))
    return render_template('admin/crear_rifa.html')

@app.route('/admin/rifa/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    if request.method == 'POST':
        rifa.nombre = request.form.get('nombre')
        rifa.premio = request.form.get('premio')
        rifa.informacion = request.form.get('informacion')
        
        fecha_str = request.form.get('fecha')
        if fecha_str:
             try: rifa.fecha_fin = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
             except: pass
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '':
                config = AppConfig()
                filename = f"rifa_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(config.get_rifa_upload_folder, filename))
                rifa.imagen = f"img/rifas/{filename}"

        db.session.commit()
        flash('Rifa actualizada')
        return redirect(url_for('gestionar_rifas'))
    return render_template('admin/editar_rifa.html', rifa=rifa)

@app.route('/admin/rifa/eliminar/confirmar/<int:id>')
@login_required
@admin_required
def confirmar_eliminar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    return render_template('admin/confirmar_eliminar_rifa.html', rifa=rifa)

@app.route('/admin/rifa/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    if rifa.imagen:
        config = AppConfig()
        filename = os.path.basename(rifa.imagen)
        path = os.path.join(config.get_rifa_upload_folder, filename)
        if os.path.exists(path):
            try: os.remove(path)
            except: pass
    db.session.delete(rifa)
    db.session.commit()
    flash('Rifa eliminada')
    return redirect(url_for('gestionar_rifas'))

# --- SOCIO / DONAR ---

@app.route('/hazte-socio', methods=['GET', 'POST'])
def hazte_socio():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Simplificado para mantener funcionalidad base
        current_user.es_socio = True
        db.session.commit()
        flash('¡Ya eres socio!')
        return redirect(url_for('dashboard'))
    return render_template('hazte_socio.html')

@app.route('/hazte-voluntario', methods=['GET', 'POST'])
def hazte_voluntario():
    if request.method == 'POST':
        flash('Solicitud recibida')
        return redirect(url_for('index'))
    return render_template('hazte_voluntario.html')

@app.route('/donar', methods=['GET', 'POST'])
def donar():
    if request.method == 'POST':
        flash('Gracias por donar (Simulado)')
        return redirect(url_for('dashboard'))
    return render_template('donar.html')

# --- AUTH ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre', email.split('@')[0])
        password = request.form.get('password')
        
        if Usuario.query.filter_by(correo_electronico=email).first():
            flash('Correo ya registrado')
        else:
            u = Usuario(
                nombre_usuario=nombre,
                correo_electronico=email,
                contrasena_hash=generate_password_hash(password, method='pbkdf2:sha256'),
                es_socio=False
            )
            db.session.add(u)
            db.session.commit()
            login_user(u)
            return redirect(url_for('dashboard'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        u = Usuario.query.filter_by(correo_electronico=email).first()
        if u and check_password_hash(u.contrasena_hash, password):
            login_user(u)
            return redirect(url_for('dashboard'))
        else:
            flash('Login incorrecto')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    entradas = Entrada.query.filter_by(id_comprador=current_user.id).all()
    return render_template('dashboard.html', user=current_user, entradas=entradas)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        current_user.nombre_usuario = request.form.get('nombre')
        current_user.correo_electronico = request.form.get('email')
        current_user.dni_nif = request.form.get('dni')
        db.session.commit()
        flash('Perfil actualizado')
        return redirect(url_for('dashboard'))
    return render_template('editar_perfil.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- VALIDACIÓN QR ---

@app.route('/admin/escanear_qr')
@login_required
@admin_required
def escanear_qr():
    return render_template('admin/escanear_qr.html')

@app.route('/api/validar_qr', methods=['POST'])
@login_required
@admin_required
def validar_qr_api():
    # Simplificado, misma logica
    data = request.get_json()
    qr_content = data.get('qr_content')
    if not qr_content or not qr_content.startswith('TICKET:'):
        return jsonify({'valid': False, 'message': 'Formato inválido'}), 400
    
    uuid_part = qr_content.split(':', 1)[1]
    entrada = Entrada.query.filter_by(codigo_qr=f"img/qrcodes/qr_{uuid_part}.png").first()
    
    if entrada:
        return jsonify({'valid': True, 'mensaje': 'Válida', 'evento': entrada.evento.nombre_evento, 'asistente': Usuario.query.get(entrada.id_comprador).nombre_usuario})
    else:
        return jsonify({'valid': False, 'message': 'No encontrada'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Evento.query.first():
            # Demo Data
            e = Evento(
                nombre_evento="Gala Inicio", 
                localizacion="Marbella", 
                fecha=datetime(2026,1,1), 
                precio=50.0, 
                informacion="Demo"
            )
            db.session.add(e)
            db.session.commit()
    app.run(debug=True)