import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Usuario, Evento, Entrada, Rifa, Boleto, MetaRecaudacion, Donacion
from patterns import AppConfig, EmailNotificationObserver
from services import FundraisingFacade

# Configuracion Singleton inicial
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'baseDatos', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Rutas de subida
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'eventos')
app.config['RIFA_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'rifas')
app.config['QR_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'qrcodes')

app_config = AppConfig()
app_config.init_app(app)

db.init_app(app)
facade = FundraisingFacade()

# [OBSERVER] Registrar observadores
facade.attach(EmailNotificationObserver())


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
    meta_activa = facade.get_active_meta()
    recaudado, porcentaje = facade.calculate_progress(meta_activa)
    return render_template('index.html', meta=meta_activa, recaudado=recaudado, porcentaje=porcentaje)

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
        try:
            cantidad_boletos = int(request.form.get('cantidad', 1))
        except ValueError:
            cantidad_boletos = 1
            
        metodo_pago = request.form.get('metodo_pago')
        
        success, msg = facade.purchase_raffle_tickets(
            raffle_id=id,
            quantity=cantidad_boletos,
            method=metodo_pago,
            form_data=request.form,
            user_id=current_user.id
        )

        if success:
             flash(f'Compra exitosa: {msg}')
             return redirect(url_for('dashboard'))
        else:
            flash(f"Error: {msg}")
            return render_template('participar_rifa.html', rifa=rifa)

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

        success, msg = facade.purchase_ticket(
            event_id=id_evento,
            quantity=cantidad_entradas,
            method=metodo_pago,
            form_data=request.form,
            user_id=current_user.id
        )
        
        if success:
            flash(f'¡Pago exitoso! {msg}')
            return redirect(url_for('dashboard'))
        else:
            flash(f"Pago fallido: {msg}")
            return render_template('pago_entrada.html', evento=evento)

    return render_template('pago_entrada.html', evento=evento)

# --- RUTAS DE ADMINISTRACIÓN DE EVENTOS ---

@app.route('/admin/evento/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_evento():
    if request.method == 'POST':
        success, msg = facade.create_event(request.form, request.files.get('imagen'))
        if success:
            flash(msg)
            return redirect(url_for('eventos'))
        else:
            flash(f"Error: {msg}")
            
    return render_template('admin/crear_evento.html')

@app.route('/admin/evento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_evento(id):
    evento = Evento.query.get_or_404(id)
    if request.method == 'POST':
        success, msg = facade.update_event(id, request.form, request.files.get('imagen'))
        if success:
             flash(msg)
             return redirect(url_for('ver_evento', id=id))
        else:
             flash(f"Error: {msg}")
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
    success, msg = facade.delete_event(id)
    flash(msg)
    return redirect(url_for('eventos'))

@app.route('/admin/evento/clonar/<int:id>')
@login_required
@admin_required
def clonar_evento(id):
    success, msg = facade.clone_event(id)
    flash(msg)
    return redirect(url_for('eventos'))

# --- RUTAS DE ADMINISTRACIÓN GENERAL ---

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

# --- RUTAS DE ADMINISTRACIÓN DE METAS (CRUD) ---

@app.route('/admin/metas')
@login_required
@admin_required
def gestionar_metas():
    # Usando el facade para obtener datos procesados
    datos_metas = facade.get_all_metas_with_progress()
    return render_template('admin/gestionar_metas.html', metas=datos_metas)

@app.route('/admin/meta/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_meta():
    if request.method == 'POST':
        success, msg = facade.create_meta(request.form, request.files.get('imagen'))
        flash(msg)
        if success:
            return redirect(url_for('gestionar_metas'))
    return render_template('admin/crear_meta.html')

@app.route('/admin/meta/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_meta(id):
    meta = facade.get_meta_by_id(id)
    if request.method == 'POST':
        success, msg = facade.update_meta(id, request.form, request.files.get('imagen'))
        flash(msg)
        if success:
            return redirect(url_for('gestionar_metas'))
    return render_template('admin/editar_meta.html', meta=meta)

@app.route('/admin/meta/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_meta(id):
    success, msg = facade.delete_meta(id)
    flash(msg)
    return redirect(url_for('gestionar_metas'))

@app.route('/meta/<int:id>')
def ver_meta(id):
    meta = facade.get_meta_by_id(id)
    recaudado, porcentaje = facade.calculate_progress(meta)
    return render_template('ver_meta.html', meta=meta, recaudado=recaudado, porcentaje=porcentaje)

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
        success, msg = facade.create_raffle(request.form, request.files.get('imagen'))
        flash(msg)
        if success:
            return redirect(url_for('gestionar_rifas'))
    return render_template('admin/crear_rifa.html')

@app.route('/admin/rifa/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_rifa(id):
    rifa = Rifa.query.get_or_404(id)
    if request.method == 'POST':
        success, msg = facade.update_raffle(id, request.form, request.files.get('imagen'))
        flash(msg)
        if success:
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
    success, msg = facade.delete_raffle(id)
    flash(msg)
    return redirect(url_for('gestionar_rifas'))

# --- SOCIO / DONAR ---

@app.route('/hazte-socio', methods=['GET', 'POST'])
def hazte_socio():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
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
        tipo_form = request.form.get('tipo_formulario')
        
        if tipo_form == 'dona_ahora':
            metodo_pago = request.form.get('metodo_pago')
            try:
                cantidad = float(request.form.get('cantidad', 0))
            except ValueError:
                flash('Cantidad inválida')
                return redirect(url_for('donar'))

            user_id = current_user.id if current_user.is_authenticated else None
            success, msg = facade.process_donation(cantidad, metodo_pago, request.form, user_id)
            
            if success:
                flash(f"¡Gracias por tu donación de {cantidad}€! ({msg})")
                return redirect(url_for('index'))
            else:
                flash(f"Error en la donación: {msg}")

        elif tipo_form == 'transferencia':
            cantidad = request.form.get('cantidad')
            nombre = request.form.get('nombre')
            flash(f"Hemos registrado tu aviso de transferencia de {cantidad}€. Lo verificaremos pronto. Gracias, {nombre}.")
            return redirect(url_for('index'))
            
    return render_template('donar.html')

# --- AUTHENTICATION ---

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
    boletos = Boleto.query.filter_by(id_comprador=current_user.id).all()
    return render_template('dashboard.html', user=current_user, entradas=entradas, boletos=boletos)

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
    data = request.get_json()
    valid, message, details = facade.validate_qr(data.get('qr_content'))
    
    if valid:
        return jsonify({'valid': True, 'mensaje': message, **details})
    else:
        return jsonify({'valid': False, 'message': message}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Evento.query.first():
            e = Evento(
                nombre_evento="Gala Inicio", 
                localizacion="Marbella", 
                fecha=datetime(2026,1,1), 
                precio=50.0, 
                informacion="Demo"
            )
            db.session.add(e)
            db.session.commit()
    app.run(debug=True, ssl_context='adhoc')
